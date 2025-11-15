from consts import *
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from youtube_bot_src.keyboards.AdminKeyboards import InlineAdminKeyboards
from youtube_bot_src.services.db import Users_class, Sharing_class
from youtube_bot_src.routers.callBack.listsCallback import ads_routers
from youtube_bot_src.services.scripts.utils import send_ads_for_admin

router = Router(name=__name__)
router.include_router(ads_routers)


@router.callback_query(lambda call: call.data.split(' ')[0] == "mailing")
async def mailing_list(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("uxarkeq dzer uzac median ev kceq texty", reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(ADS_Mailing.mailing_media)


@router.callback_query(lambda call: call.data.split(' ')[0] == "sharing")
async def patron(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("uxarkeq dzer uzac median ev kceq texty", reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(ADS_Sharing.sharing_media)


@router.callback_query(lambda call: call.data.split(' ')[0] == "subs_on_channel_ads")
async def sharing(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("greq kanali texty ev nkary", reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(SubsAds_storage.SubsAds_media)


@router.callback_query(lambda call: call.data.split(' ')[0] == "statistics")
async def statistics(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    user_count = len(Users_class.get_all())
    await call.message.answer(f"""
user count: {user_count}
    """)


@router.callback_query(lambda call: call.data.split(' ')[0] == "ref")
async def statistics_statistics(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("refs")


@router.callback_query(lambda call: call.data.split(' ')[0] == "settings")
async def statistics_statistics(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("settings")


@router.callback_query(lambda call: call.data.split(' ')[0] == "clear_state")
async def statistics(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await state.clear()
    await call.message.answer("admini hnaravorutyunery", reply_markup=InlineAdminKeyboards.main_functions())


@router.callback_query(lambda call: call.data.split(' ')[0] == "ads_list")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    await call.message.answer("@ntreq govazdi tesaky", reply_markup=InlineAdminKeyboards.ads_list())


@router.callback_query(lambda call: call.data.split(' ')[0] == "show_list")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"ADMIN CLICK ON {call.data}")

    data = call.data.split(' ')
    if data[1] == "sharing_show":
        ads = Sharing_class.get_all()[0]
        await send_ads_for_admin(
            admin_id=call.message.chat.id,
            ads=ads,
            buttons=InlineAdminKeyboards.show_ads_sharing_list(
                index=0,
                active=ads.active
            )
        )
