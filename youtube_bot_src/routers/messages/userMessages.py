from youtube_bot_src.filters.MyFilters import IsTrueYoutubeLink, IsTrueTikTokLink, IsTrueInstagramLink
from youtube_bot_src.services.downloads.YoutubeDownloadClass import NewYoutubeDownloadClass, get_channel_info
from youtube_bot_src.services.downloads.TiktokDownloadClass import TiktokDownloadClass
from youtube_bot_src.services.downloads.InstagramDownloadClass import InstagramDownloadClass
from youtube_bot_src.services import db
from aiogram import F, types
from consts import *

router = Router()


@router.message(IsTrueYoutubeLink())
async def msgs(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    error_count = 0
    while error_count < 4:
        try:
            download_video_exemplar = NewYoutubeDownloadClass(chat_id=msg.from_user.id, state=state, url=msg.text)
            message = await msg.answer_photo(
                reply_markup=user_keyboards.start(
                    quality=download_video_exemplar.video_quality,
                    url=download_video_exemplar.video_id,
                    language=user_data.get('language')),
                photo=types.URLInputFile(download_video_exemplar.photo),
                caption=SendMessagesUser.send_video_data(user_data.get("language")).format(
                    title=download_video_exemplar.title + "\n", loading_bar="")
            )
            await state.update_data({"message_id": message.message_id})
            break
        except Exception:
            error_count += 1
    else:
        await msg.answer_photo(
            photo=aiogram_types.FSInputFile(f"{PATH}/media/bot/YoutubeError.jpg"),
            caption=SendMessagesUser.send_search_error(user_data.get("language")),
            parse_mode=ParseMode.HTML
        )



@router.message(IsTrueTikTokLink())
async def download_tiktok(msg: types.Message, state: FSMContext):
    try:
        download_now[msg.from_user.id]
    except KeyError:
        download_now[msg.from_user.id] = False
    user_data = await state.get_data()
    download_video_exemplar = TiktokDownloadClass(url=msg.text, chat_id=msg.from_user.id, state=state)
    download_now_count_true = 0

    if download_now[msg.from_user.id] is False:
        message = await msg.answer(f"{SendMessagesUser.sending_loading(user_data.get('language'))[0]} □□□□□□□□")
        download_video_exemplar.sending_index += 1
        await state.update_data({"message_id": message.message_id})
        download_now[msg.from_user.id] = True
        await download_video_exemplar.download_video()

    user_data = await state.get_data()

    while download_now_count_true <= 4:
        active_user_count = 0
        while active_user_count < len(download_now):
            active_user_count += 1

        logger_bot.info(active_user_count)
        if download_now[msg.from_user.id] is False:
            try:
                await bot.delete_message(chat_id=msg.chat.id, message_id=user_data.get("message_id"))
            except as_exceptions.TelegramBadRequest:
                pass
            break
        download_now_count_true += 1
        await asyncio.sleep(1)
    else:
        try:
            await bot.delete_message(chat_id=msg.chat.id, message_id=user_data.get("message_id"))
        except as_exceptions.TelegramBadRequest:
            pass
        download_now[msg.from_user.id] = False


@router.message(IsTrueInstagramLink())
async def download_instagram(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get('language')

    msgs = SendMessagesUser.download_process(language, type_d="video")
    message = await msg.answer(f"{msgs[0]} □□□□□")

    await state.update_data({'message_id': message.message_id})
    instagram_data = InstagramDownloadClass(url=msg.text, chat_id=msg.from_user.id, state=state)
    await instagram_data.download_video()
    # loop = asyncio.get_event_loop()
    # loop.create_task(instagram_data.loading_download_message(msgs[0]))
    # status = await instagram_data.download()

    # if status != 200:
    #     pass



@router.message(F.text == '👤 subs')
async def follows(msg: types.Message, state: FSMContext):
    await msg.delete()
    user_data_subs = db.Subs_class.get_channel_by_user_id(msg.chat.id)
    if len(user_data_subs) > 0:
        user_data = await state.get_data()
        info = get_channel_info(channel_id=user_data_subs[0].get('channel_id'))

        await msg.answer_photo(
            photo=types.URLInputFile(info.get('photo')),
            reply_markup=user_keyboards.follow(
                index=0,
                notif=user_data_subs[0].get('notif'),
                channel_id=user_data_subs[0].get('channel_id'),
                language=user_data.get("language")))


@router.message(F.text == '🏳️ language')
async def language(msg: types.Message, state: FSMContext):
    await msg.delete()
    user_data = db.Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    await msg.answer(SendMessagesUser.language(user_data.lang), reply_markup=user_keyboards.langusage())


@router.message(F.text == '🔎 search')
async def search(msg: types.Message, state: FSMContext):
    await msg.delete()
    state_data = await state.get_data()
    await msg.answer(SendMessagesUser.send_search(state_data.get('language')))
