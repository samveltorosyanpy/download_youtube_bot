from youtube_bot_src.services.scripts.utils import send_ads
from youtube_bot_src.keyboards.AdminKeyboards import InlineAdminKeyboards
from youtube_bot_src.services.db import Users_class, Sharing_class, SubsAds_class, Mailings_class
from consts import *

router = Router()


@router.message(ADS_Mailing.mailing_media)
async def mailing_list_start(msg: aiogram_types.Message, state: FSMContext):
    try:
        await state.update_data({"mailing_media": {"photo": msg.photo[-1].file_id}})
        if msg.caption is not None:
            await state.update_data({"mailing_text": msg.caption})
    except TypeError as err:
        print("no photo")

    try:
        await state.update_data({"mailing_media": {"video": msg.document.file_id}})
        if msg.caption is not None:
            await state.update_data({"mailing_text": msg.caption})
    except AttributeError as err:
        try:
            await state.update_data({"mailing_media": {"video": msg.video.file_id}})
            if msg.caption is not None:
                await state.update_data({"mailing_text": msg.caption})
        except AttributeError as err:
            pass
        print("no video")

    if msg.text is not None:
        await state.update_data({"mailing_text": msg.text})

    await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar",
                     reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(ADS_Mailing.mailing_buttons)


@router.message(ADS_Mailing.mailing_buttons)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    text = msg.text
    item = ' :|: '
    data = await state.get_data()
    users_mailing = Users_class.get_all()
    # users_mailing = ADMINS

    if item in text:
        ADS_BUTTONS.update({text[:text.index(item)]: text[text.index(item) + 5:]})
        await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar")
        await state.set_state(ADS_Mailing.mailing_buttons)
    elif text == '/next':
        ads_id = Mailings_class.add_mailing(text=data.get("mailing_text"),
                                            buttons=f"{ADS_BUTTONS}" or None,
                                            media=str(data.get("mailing_media")))
        ADS_BUTTONS.clear()
        await state.clear()
        await msg.answer("govazdy hajoxutyamb texadrvac e")
        user_send_count = 0
        user_block_count = 0
        user_index = 0
        ads = Mailings_class.get_by_id(ads_id)[0]
        while user_index < len(users_mailing):
            status = await send_ads(user_id=users_mailing[user_index], ads=ads)
            if status == 1:
                user_block_count += 1
                user_index += 1
                logger_bot.info(f"error sent to {users_mailing[user_index]} {user_block_count}")
                continue
            logger_bot.info(f"sent to {users_mailing[user_index]} {user_send_count}")
            user_index += 1
            user_send_count += 1
            await asyncio.sleep(1)
        await bot.send_message(ADMIN, f"Sent for {user_send_count} and block {user_block_count} Users")

    else:
        await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar")
        await state.set_state(ADS_Mailing.mailing_buttons)


@router.message(ADS_Sharing.sharing_media)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    try:
        await state.update_data({"sharing_media": {"photo": f"{msg.photo[-1].file_id}"}})
        if msg.caption is not None:
            await state.update_data({"sharing_text": msg.caption})
    except TypeError as err:
        print("no photo")

    try:
        await state.update_data({"sharing_media": {"video": f"{msg.video.file_id}"}})
        if msg.caption is not None:
            await state.update_data({"sharing_text": msg.caption})
    except AttributeError as err:
        try:
            await state.update_data({"sharing_media": {"video": f"{msg.document.file_id}"}})
        except AttributeError as err:
            print("no video")

    if msg.text is not None:
        await state.update_data({"sharing_text": msg.text})

    await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar",
                     reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(ADS_Sharing.sharing_buttons)


@router.message(ADS_Sharing.sharing_buttons)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    text = msg.text
    item = ' :|: '
    data = await state.get_data()

    if item in text:
        ADS_BUTTONS.update({text[:text.index(item)]: text[text.index(item) + 5:]})
        await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar")
        await state.set_state(ADS_Sharing.sharing_buttons)
    elif text == '/next':
        Sharing_class.add_sharing(text=data.get("sharing_text"),
                                            buttons=f"{ADS_BUTTONS}" or None,
                                            media=str(data.get("sharing_media")))
        ADS_BUTTONS.clear()
        await state.clear()
    else:
        await msg.answer("grir ays formatov '<url> :|: <button>' kam /next bac toxnelu hamar")
        await state.set_state(ADS_Sharing.sharing_buttons)


@router.message(SubsAds_storage.SubsAds_media)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    try:
        await state.update_data({"SubsAds_media": {"photo": f"{msg.photo[-1].file_id}"}})
        if msg.caption is not None:
            await state.update_data({"SubsAds_text": msg.caption})
    except TypeError as err:
        print("no photo")

    try:
        await state.update_data({"SubsAds_media": {"video": f"{msg.video.file_id}"}})
        if msg.caption is not None:
            await state.update_data({"SubsAds_text": msg.caption})
    except AttributeError as err:
        try:
            await state.update_data({"SubsAds_media": {"video": f"{msg.document.file_id}"}})
        except AttributeError as err:
            print("no video")

    if msg.text is not None:
        await state.update_data({"SubsAds_text": msg.text})

    await msg.answer("greq kanali url hascen", reply_markup=InlineAdminKeyboards.clear_state())
    await state.set_state(SubsAds_storage.SubsAds_channel_url)


@router.message(SubsAds_storage.SubsAds_channel_url)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    try:
        if requests.get(msg.text).status_code:
            await state.update_data({"SubsAds_channel_url": msg.text})
            await msg.answer("greq kanali id", reply_markup=InlineAdminKeyboards.clear_state())
            await state.set_state(SubsAds_storage.SubsAds_channel_id)
    except Exception:
        await msg.answer("url hascen sxal e greq noric", reply_markup=InlineAdminKeyboards.clear_state())
        # await state.set_state(ADS_Mailing.mailing_channel_link)


@router.message(SubsAds_storage.SubsAds_channel_id)
async def patron_list_text(msg: aiogram_types.Message, state: FSMContext):
    data = await state.get_data()
    SubsAds_class.add(channel_link=data.get("SubsAds_channel_url"), text=data.get("SubsAds_text"),
                      photo_ids=str(data.get("SubsAds_media")), channel_id=msg.text)
    await state.clear()
