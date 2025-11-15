from aiogram.filters import BaseFilter
from aiogram import exceptions
import json, requests
from youtube_bot_src.services import db
from consts import *
from youtube_bot_src.services.downloads.YoutubeDownloadClass import NewYoutubeDownloadClass

class MainFilter(BaseFilter):
    async def __call__(self, msg: aiogram_types.Message, state: FSMContext) -> bool:
        logger_bot.info(user_id=msg.chat.id, message=f"USER SEND TEXT: {msg.text}")
        try:
            await db.Users_class.add(user_id=msg.chat.id)
            logger_maria.info(user_id=msg.chat.id, message=f"ADD NEW USER BY ID {msg.chat.id}")
            await msg.answer(SendMessagesUser.language("ru"), reply_markup=user_keyboards.langusage_new())
            await state.update_data({'language': "ru"})
        except db.sqlalchemy_exc.IntegrityError:
            await state.update_data({'language': db.Users_class.get(msg.chat.id).lang})
        return True


class IsTrueYoutubeLink(BaseFilter):
    async def __call__(self, msg: aiogram_types.Message, state: FSMContext) -> bool:
        try:
            if any(x in msg.text for x in ["youtube", "youtu.be"]):
                return True
        except TypeError as err:
            logger_bot.error(msg.from_user.id, err)
        return False


class IsTrueTikTokLink(BaseFilter):
    async def __call__(self, msg: aiogram_types.Message, state: FSMContext) -> bool:
        try:
            if any(x in msg.text for x in ["tiktok.com", "vt.tiktok.com"]):
                return True
        except TypeError as err:
            logger_bot.error(msg.from_user.id, err)
        return False


class IsTrueInstagramLink(BaseFilter):
    async def __call__(self, msg: aiogram_types.Message) -> bool:
        try:
            if any(x in msg.text for x in ["www.instagram.com"]):
                return True
        except TypeError as err:
            logger_bot.error(msg.from_user.id, err)
        return False


class IsTrueAdminId(BaseFilter):
    async def __call__(self, msg: aiogram_types.Message) -> bool:
        return msg.chat.id in ADMINS





class IsUserFollowToChannels(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, call: aiogram_types.CallbackQuery, state: FSMContext) -> bool:
        channels = db.SubsAds_class.get_all_active()
        user_data = db.Users_class.get(call.from_user.id)
        if channels:
            for channel in channels:
                try:
                    chat_member = await bot.get_chat_member(user_id=call.from_user.id, chat_id=int(channel.channel_id))
                    if chat_member.status.value != 'left':
                        return True
                    elif chat_member.status.value == 'left':
                        try:
                            medias = json.loads(channel.media.replace('\'', '"'))

                            if 'photo' in medias.keys():
                                await call.answer_photo(
                                    photo=medias['photo'],
                                    caption=channel.text,
                                    reply_markup=aiogram_types.InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [aiogram_types.InlineKeyboardButton(
                                                text=SendMessagesUser.ADS_SUBMIT(user_data.lang),
                                                url=channel.channel_link)]])
                                )
                            elif 'video' in medias.keys():
                                await bot.send_video(
                                    chat_id=call.from_user.id,
                                    video=medias['video'],
                                    caption=channel.text,
                                    reply_markup=aiogram_types.InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [aiogram_types.InlineKeyboardButton(
                                                text=SendMessagesUser.ADS_SUBMIT(user_data.lang),
                                                url=channel.channel_link)]])
                                )
                            else:
                                await call.message.answer(
                                    text=channel.text,
                                    reply_markup=aiogram_types.InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [aiogram_types.InlineKeyboardButton(
                                                text=SendMessagesUser.ADS_SUBMIT(user_data.lang),
                                                url=channel.channel_link)]])
                                )
                        except AttributeError:
                            print(channel.text)
                            if channel.text:
                                await call.message.answer(
                                    text=channel.text,
                                    reply_markup=aiogram_types.InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [aiogram_types.InlineKeyboardButton(text='Subscribe', url=channel.channel_link)]])
                                )
                                print("ssssss")
                        print("finish False")

                        return False

                except exceptions.TelegramBadRequest:
                    print('aaaa')
                    await bot.send_message(ADMIN, f"{channel.channel_link} kanalum boty admin chi")
        return True
