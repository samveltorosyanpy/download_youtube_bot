from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from youtube_bot_src.keyboards import user_keyboards
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
from youtube_bot_src.services.scripts.youtube import ClassYoutube
from consts import *
from pathlib import Path
from youtube_bot_src.services.scripts.effects import Effector

router = Router(name=__name__)


@router.callback_query(lambda call: call.data.split(' ')[0].split(' ')[0] == "Effect_edit")
async def Effect_edit(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    await call.message.answer(
        SendMessagesUser.send_effects_edit(state_data, state_data.get('language')),
        reply_markup=user_keyboards.audio_edit_buttons(state_data['language'])
    )


@router.callback_query(lambda call: call.data.split(' ')[0] == "Effect_back")
async def Effect_help_back(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    await call.message.edit_text(SendMessagesUser.send_effects_edit(state_data, state_data.get('language')),
                                 reply_markup=user_keyboards.audio_edit_buttons(state_data.get('language')))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Effect_help")
async def Effect_help(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    await call.message.edit_text(
        SendMessagesUser.send_effects_edit_help(language=state_data.get('language')),
        reply_markup=user_keyboards.audio_help_back(state_data.get('language'))
    )


@router.callback_query(lambda x: x.data in ['Effect_reverb', 'Effect_8d', 'Effect_bass', 'Effect_pitch', 'Effect_speed'])
async def Effects(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()

    effect = None
    value_array = []

    if call.data == 'Effect_reverb':
        effect = 'reverb'
        value_array = [25, 35, 45, 55, 65, 75]
    elif call.data == 'Effect_bass':
        effect = 'bass'
        value_array = [4, 6, 8, 10, 12, 14]
    elif call.data == 'Effect_8d':
        effect = '8d'
        value_array = [50, 100, 150, 200, 300, 350]
    elif call.data == 'Effect_pitch':
        effect = 'pitch'
        value_array = [-6, -4, -2, 2, 4, 6]
    elif call.data == 'Effect_speed':
        effect = 'speed'
        value_array = [0.6, 0.7, 0.8, 1.2, 1.3, 1.4]

    await call.message.edit_text(SendMessagesUser.send_effect_edit_instruction(state_data.get('language')),
                                 reply_markup=user_keyboards.audio_edit_effects(value_array, effect,
                                                                                state_data.get('language')))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Effect_add")
async def Effect_add(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    await call.answer('✅')

    state_data = await state.get_data()
    data = call.data.split(' ')

    await state.update_data({data[2]: float(data[1])})
    await call.message.edit_text(SendMessagesUser.send_effects_edit(
        await state.get_data(), state_data.get('language')),
        reply_markup=user_keyboards.audio_edit_buttons(state_data.get('language')))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Effect_confirm")
async def Effect_confirm(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    await call.message.answer(SendMessagesUser.send_transcription(state_data['language']))


    # video_data = ClassYoutube(state_data.get('video_url'))
    # title = video_data.Download_audio()
    #
    # file_path = Path(f'{PATH}/media/audio/{title}.mp3')
    # file_path_edited = Path(f'{PATH}/media/audio/{title}_edited.mp3')
    #
    # edited_file = Effector.add_effects(
    #     input_path=str(file_path),
    #     final_path=str(file_path_edited),
    #     reverberance=state_data.get('reverb') or 0,
    #     bass=state_data.get('bass') or 0,
    #     pitch=state_data.get('pitch') or 0,
    #     speed=state_data.get('speed') or 1,
    # )
    #
    # await call.bot.send_audio(
    #     chat_id=call.from_user.id,
    #     title=video_data.title,
    #     thumbnail=types.FSInputFile(f"{PATH}/media/bot/logo.jpg"),
    #     audio=types.FSInputFile(path=edited_file),
    #     caption=SendMessagesUser.send_audio(language=state_data['language']),
    #     reply_markup=user_keyboards.edit_mp3(language=state_data['language'])
    # )
    # file_path.unlink()
    # file_path_edited.unlink()
    await state.clear()








