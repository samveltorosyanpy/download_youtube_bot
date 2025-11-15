from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
from youtube_bot_src.services.db import Users_class
from consts import *
from youtube_bot_src.keyboards.UserKeyboards import ReplyUserKeyboard
from aiogram.enums.parse_mode import ParseMode


router = Router(name=__name__)


@router.callback_query(lambda call: call.data.split(' ')[0] == "change_language")
async def change_language(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    Users_class.update_by_id(user_id=call.from_user.id, lang=data[1])
    await state.update_data({'language': data[1]})
    await call.message.answer(SendMessagesUser.change_language(data[2], data[1]))


@router.callback_query(lambda call: call.data.split(' ')[0] == "change_language_new")
async def change_language(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    Users_class.update_by_id(user_id=call.from_user.id, lang=data[1])
    await state.update_data({'language': data[1]})
    texts = SendMessagesUser.start(data[1])
    logger_bot.info(texts)
    await call.message.answer_photo(
        photo=types.FSInputFile(f"{PATH}/media/bot/start_videos/{texts[1]}"),
        caption=texts[0],
        reply_markup=ReplyUserKeyboard.main(),
        parse_mode=ParseMode.HTML
    )



