from aiogram import types, Router
from youtube_bot_src.services.downloads.YoutubeDownloadClass import search_list_in_youtube
from consts import *

router = Router(name=__name__)


@router.message()
async def search(msg: types.Message, state: FSMContext):
    await msg.delete()
    user_data = await state.get_data()
    videos = await search_list_in_youtube(1, msg.text)
    if len(videos) > 0:
        message = await msg.answer(msg.text, reply_markup=user_keyboards.search_list(videos, 1, 2, msg.text))
        await state.update_data({"message_id": message.message_id})
    else:
        await msg.answer_photo(
            photo=types.FSInputFile(f"{PATH}/media/bot/YoutubeError.jpg"),
            caption=SendMessagesUser.send_search_error(user_data.get("language")),
            parse_mode=ParseMode.HTML
        )
