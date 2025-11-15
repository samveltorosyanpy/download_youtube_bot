import asyncio
from datetime import datetime as dt, timedelta, date as week_day
import shutil
from youtube_bot_src.settings import STATISTIC
from youtube_bot_src.services.db import Mailings_class, Sharing_class, SubsAds_class, Subs_class
from youtube_bot_src.services.scripts.youtube import ClassYoutube, get_last_video_by_channel_id
from aiogram import exceptions, types
from youtube_bot_src.services.downloads.YoutubeDownloadClass import NewYoutubeDownloadClass, get_base_info_by_video_id_from_youtube
from youtube_bot_src.services.db import Users_class
from aiogram.fsm.storage.base import StorageKey
from consts import *

async def mailing_visits_insert_now_data():
    while STATISTIC:
        logger_bot.info("check new statistic")
        Mailings_ids = Mailings_class.get_all_active()
        users = Users_class.get_all()

        for channel in Mailings_ids:
            channel_id = channel.channel_id
            members_count = await bot.get_chat_member_count(channel_id)
            count = 0
            if members_count != channel.count:
                for user in users:
                    try:
                        chat_member = await bot.get_chat_member(user_id=user, chat_id=int(channel_id))
                        if chat_member.status.value in ['creator', 'member', 'administrator']:
                            count += 1
                    except exceptions.TelegramBadRequest:
                        pass
                Mailings_class.mailing_list_update(channel_id=channel_id, members=count, count=members_count)
        await asyncio.sleep(100)


async def check_new_video():
    while True:
        logger_bot.info("RUN CHECK NEW VIDEO IN YOUTUBE")
        subs_data = Subs_class.get_all_unic_channel_id()
        for channel in subs_data:
            last_video_id_in_channel = get_last_video_by_channel_id(channel_id=channel.get('channel_id'))
            if (last_video_id_in_channel != channel.get('last_publish_video_id') and last_video_id_in_channel is not None):
                new_video_data = get_base_info_by_video_id_from_youtube(f"https://www.youtube.com/watch?v={last_video_id_in_channel}")
                follows_users = Subs_class.get_all_user_id_follow_channel(channel.get('channel_id'))
                for users in follows_users:
                    user_d = Users_class.get(user_id=users["user_id"])
                    notif = False if bool(users['notif']) is True else True

                    try:
                        message = await bot.send_photo(
                            chat_id=users['user_id'],
                            disable_notification=notif,
                            photo=types.URLInputFile(new_video_data["photo"]),
                            reply_markup=user_keyboards.start(
                                quality=["1080p", "720p", "480p", "360p", "144p"],
                                url=last_video_id_in_channel,
                                language=user_d.lang),
                            caption=SendMessagesUser.send_video_data("ru").format(
                                title=new_video_data["title"] + "\n", loading_bar=""))
                    except KeyError:
                        break
                    global_user_storage: FSMContext = FSMContext(
                        storage=dp.storage,
                        key=StorageKey(
                            chat_id=message.chat.id,
                            user_id=message.from_user.id,
                            bot_id=bot.id))

                    await global_user_storage.update_data({"message_id": message.message_id})
                    td = await global_user_storage.get_data()
                    logger_bot.info(td)
                    await asyncio.sleep(0.1)

                Subs_class.update_by_id_all(channel.get('channel_id'), last_publish_video_id=last_video_id_in_channel)

        await asyncio.sleep(10000)


async def check_is_dead():
    while True:
        users = Users_class.get_all()
        for user in users:
            if Users_class.get(user_id=user).is_dead is True:
                Users_class.update_by_id(user_id=user, is_dead=False)

        await asyncio.sleep(100)


async def checking_file_datetime():
    while True:
        logger_bot.info("RUN C. F. D. T.")
        items = os.listdir(f"{PATH}/media/videos/youtube_videos/")
        for item in items:
            file_path = f"{PATH}/media/videos/youtube_videos/{item}"
            try:
                # create_at = dt.fromtimestamp(os.path.getmtime(file_path))
                # if create_at > dt.now() + timedelta(days=2):
                os.remove(file_path)
            except FileNotFoundError:
                logger_bot.error(f"{file_path} cud not delete")

        await asyncio.sleep(88400)


async def create_database_backup_file():
    while True:
        today = week_day.today().strftime("%A")
        logger_bot.info(f"RUN B. W.")
        if today == "Sunday":
            data_rows = {
                'Mailings_backup': Mailings_class.get_backup(),
                'SubsAds_backup': SubsAds_class.get_backup(),
                'Sharing_backup': Sharing_class.get_backup(),
                'Users_backup': Users_class.get_backup(),
                'Subs_backup': Subs_class.get_backup()
            }

            start_date = dt.now()
            end_date = start_date + timedelta(weeks=1)
            path_name = f"{PATH}/backups/{start_date}-{end_date}"
            logger_bot.info(f"Created backup file for {start_date}-{end_date}")
            for data in data_rows:
                if os.path.exists(path_name) is False:
                    os.mkdir(path_name)
                file_name = f"{path_name}/{data}.csv"
                with open(file_name, "w"):
                    for s in data_rows[data]:
                        with open(file_name, "a") as f:
                            f.write(','.join([str(elem) for elem in s]))

            shutil.make_archive(path_name, "zip", path_name)
            await bot.send_document(BACKUP_IDS, types.FSInputFile(f"{path_name}.zip"))
            if os.path.exists(f"{path_name}.zip"):
                shutil.rmtree(path_name)

        await asyncio.sleep(5000)
