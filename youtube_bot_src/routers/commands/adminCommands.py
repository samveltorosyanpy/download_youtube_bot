from consts import *
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from youtube_bot_src.filters.MyFilters import IsTrueAdminId
from youtube_bot_src.keyboards.AdminKeyboards import InlineAdminKeyboards
from consts import ADS_Mailing

router = Router(name=__name__)
router.message.filter(IsTrueAdminId())


@router.message(Command(commands=['admin']))
async def command_addAds(msg: types.Message, state: FSMContext):
    await msg.answer("admini hnaravorutyunery", reply_markup=InlineAdminKeyboards.main_functions())


# @router.message(Command(commands=['test_mailing']))
# async def command_addAds(msg: types.Message, state: FSMContext):
#     await msg.answer("uxarki cankacac namak")
#     await state.set_state(ADS_Mailing.forvord)


# @router.message(ADS_Mailing.forvord)
# async def patron_list_text(msg: types.Message, state: FSMContext):
#     await bot.forward_message(from_chat_id=ADMIN, message_id=msg.message_id, chat_id=ADMIN)
