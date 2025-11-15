from aiogram import types, Router
from youtube_bot_src.services.downloads.TiktokDownloadClass import TiktokDownloadClass
from consts import *

router = Router(name=__name__)


@router.callback_query(lambda call: call.data.split(' ')[0] == "download_tiktok_mp3")
async def download_tiktok_mp3(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")
    data = call.data.split(' ')
    url = f"https://www.tiktok.com/@ea7.ocean/video/{data[-1]}"
    user_data = await state.get_data()
    download_now_count_true = 0

    if download_now[call.from_user.id] is False:
        download_now[call.from_user.id] = True
        message = await call.message.answer(f"{SendMessagesUser.sending_loading(user_data.get('language'))[0]} □□□□□□□□")
        video_data = TiktokDownloadClass(url=url, chat_id=call.from_user.id, state=state)
        video_data.sending_index += 1

        await state.update_data({"message_id": message.message_id})
        await video_data.download_mp3()
    else:
        return

    user_data = await state.get_data()

    while download_now_count_true <= 4:
        logger_bot.info(download_now[call.from_user.id])
        if download_now[call.from_user.id] is False:
            try:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=user_data.get("message_id"))
            except as_exceptions.TelegramBadRequest:
                pass
            break
        download_now_count_true += 1
        await asyncio.sleep(1)
    else:
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=user_data.get("message_id"))
        except as_exceptions.TelegramBadRequest:
            pass
        download_now[call.from_user.id] = False
