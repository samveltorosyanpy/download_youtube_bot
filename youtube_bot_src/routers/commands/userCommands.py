from consts import *
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from youtube_bot_src.services.db import Subs_class
from youtubesearchpython import Channel as Channel2
from youtube_bot_src.keyboards import user_keyboards
from aiogram.filters import Command
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
from youtube_bot_src.keyboards.UserKeyboards import ReplyUserKeyboard
from youtube_bot_src.services.db.models.Users import Users_class
from youtube_bot_src.services.logger import logger_bot
from aiogram.enums.parse_mode import ParseMode

router = Router(name=__name__)


@router.message(Command(commands=['start', "Start"]))
async def command_start(msg: types.Message, state: FSMContext):
    logger_bot.info(user_id=msg.chat.id, message="Enter /start command")
    user_data = Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    texts = SendMessagesUser.start(user_data.lang)
    logger_bot.info(texts)
    await msg.answer_photo(
        photo=types.FSInputFile(f"{PATH}/media/bot/start_videos/{texts[1]}"),
        caption=texts[0],
        reply_markup=ReplyUserKeyboard.main(),
        parse_mode=ParseMode.HTML
    )


@router.message(Command(commands=['help']))
async def command_start(msg: types.Message, state: FSMContext):
    user_data = Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    texts = SendMessagesUser.help(user_data.lang)
    logger_bot.info(texts)
    await msg.answer_photo(
        photo=types.FSInputFile(f"{PATH}/media/bot/help_videos/{texts[1]}"),
        caption=texts[0],
        parse_mode=ParseMode.HTML
    )


@router.message(Command(commands=['language']))
async def command_start(msg: types.Message, state: FSMContext):
    user_data = Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    await msg.answer(SendMessagesUser.language(user_data.lang), reply_markup=user_keyboards.langusage())


@router.message(Command(commands=['channel']))
async def command_start(msg: types.Message, state: FSMContext):
    user_data = Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    await msg.answer_video(
        video=types.FSInputFile(f"{PATH}/media/bot/IMG_0329.MP4"),
        caption=SendMessagesUser.channel(user_data.lang),
        reply_markup=user_keyboards.channel()
    )


@router.message(Command(commands=['subs']))
async def command_follows(msg: types.Message, state: FSMContext):
    logger_bot.info(message=f"{msg.chat.id}, {msg.from_user.id}")
    user_data_subs = Subs_class.get_channel_by_user_id(msg.chat.id)
    user_data = Users_class.get(msg.chat.id)
    await state.update_data({'language': user_data.lang})
    x = 0
    while x < 5:
        try:
            channel2 = Channel2.get(user_data_subs[0].get('channel_id'))
            try:
                image = types.URLInputFile(channel2['banners'][-1]['url'])
            except Exception:
                image = types.URLInputFile(channel2['thumbnails'][-1]['url'])

            await msg.answer_photo(
                photo=image, reply_markup=user_keyboards.follow(
                    index=0, notif=user_data_subs[0].get('notif'),
                    channel_id=user_data_subs[0].get('channel_id'),
                    language=user_data.lang)
            )
            x = 0
            break
        except TypeError:
            x += 1
        except IndexError:
            await msg.answer(SendMessagesUser.not_follow_channel(user_data.lang))
            break
    else:
        print(f"TypeError: 'NoneType' sh"
              f"ow_channels({user_data_subs[0].get('channel_id')})")



