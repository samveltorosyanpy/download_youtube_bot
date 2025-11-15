from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from youtube_bot_src.keyboards.AdminKeyboards import InlineAdminKeyboards
from youtube_bot_src.services.db import Sharing_class
from youtube_bot_src.services.scripts.utils import send_ads_for_admin
from consts import *
router = Router(name=__name__)


@router.callback_query(lambda call: call.data.split(' ')[0] == "show_list_sharing")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    data = call.data.split(' ')
    ads = Sharing_class.get_all()
    index = int(data[2])

    if data[1] == "delete":
        Sharing_class.delete_by_id(ads[index].id)
        ads.pop(index)
    elif data[1] == "active":
        active = False if data[3] == "active" else True
        Sharing_class.update_by_id(ads[index].id, active=active)
        ads[index].active = active

    if int(data[2]) == -1:
        index = len(ads) - 1
    elif int(data[2]) == len(ads):
        index = 0

    await call.message.delete()
    await send_ads_for_admin(
        admin_id=call.message.chat.id,
        ads=ads[index],
        buttons=InlineAdminKeyboards.show_ads_sharing_list(
            index=index,
            active=ads[index].active
        )
    )
