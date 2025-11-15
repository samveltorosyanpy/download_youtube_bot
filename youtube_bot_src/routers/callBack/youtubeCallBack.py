from youtube_bot_src.services.scripts.patrons import CheckAdsForDownload
from aiogram import types, Router
from youtube_bot_src.services.scripts.youtube import ClassYoutube, get_last_video_by_channel_id, search_list_in_youtube
from youtubesearchpython import Channel as Channel2
from datetime import datetime
from consts import *
from youtube_bot_src.services import db
from youtube_bot_src.services.downloads.YoutubeDownloadClass import NewYoutubeDownloadClass, get_channel_info

router = Router(name=__name__)


@router.callback_query(lambda call: call.data.split(' ')[0] == "download_mp3")
async def download_mp3(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    user_data = await state.get_data()
    download_now_count_true = 0
    url = f"https://www.youtube.com/watch?v={data[-1]}"
    download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state, url=url)
    try:
        download_now[call.from_user.id]
    except KeyError:
        download_now[call.from_user.id] = False

    if download_now[call.from_user.id] is False:
        download_now[call.from_user.id] = True
        await download_video_exemplar.download_mp3()
        await CheckAdsForDownload(call.message.chat.id)

    while download_now_count_true <= 4:
        user_data = await state.get_data()
        if download_now[call.from_user.id] is False:
            await download_video_exemplar.edit_photo_safely(
                message_id=user_data.get("message_id"),
                text=SendMessagesUser.send_video_data(user_data.get("language")).format(
                    title=download_video_exemplar.title, loading_bar=""),
                photo=download_video_exemplar.photo)
            break
        download_now_count_true += 1
        await asyncio.sleep(1)
    else:
        download_now[call.from_user.id] = False
        await download_video_exemplar.edit_reply_markup_safely(
            message_id=user_data.get('message_id'),
            reply_markup=user_keyboards.start(
                quality=download_video_exemplar.video_quality,
                url=download_video_exemplar.video_id, language=user_data.get('language')))


@router.callback_query(lambda call: call.data.split(' ')[0] == "download_video")
async def download_video(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")
    logger_bot.info(download_now)

    try:
        download_now[call.from_user.id]
    except KeyError:
        download_now[call.from_user.id] = False

    if download_now[call.from_user.id] is False:
        data = call.data.split(' ')
        url = f"https://www.youtube.com/watch?v={data[-1]}"
        download_turn.append(f"{call.from_user.id}_{url}")
        download_now[call.from_user.id] = True
        user_data = await state.get_data()
        quality = int(data[1][:-1])
        download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state, url=url)
        await download_video_exemplar.download_video(quality)
        await CheckAdsForDownload(call.message.chat.id)
    else:
        return

    download_now_count_true = 0
    while download_now_count_true <= 4:
        user_data = await state.get_data()
        logger_bot.info(download_now)
        if download_now[call.from_user.id] is False:
            await download_video_exemplar.edit_photo_safely(
                message_id=user_data.get("message_id"),
                text=SendMessagesUser.send_video_data(user_data.get("language")).format(
                title=download_video_exemplar.title,
                loading_bar=""),
                photo=download_video_exemplar.photo)
            break
        download_now_count_true += 1
        await asyncio.sleep(1)
    else:
        download_now[call.from_user.id] = False
        await download_video_exemplar.edit_reply_markup_safely(
            message_id=user_data.get('message_id'),
            reply_markup=user_keyboards.start(
                quality=download_video_exemplar.video_quality,
                url=download_video_exemplar.video_id, language=user_data.get('language')))


@router.callback_query(lambda call: call.data.split(' ')[0] == "back_to_main")
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    url = f"https://www.youtube.com/watch?v={data[-1]}"
    user_data = await state.get_data()
    download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state, url=url)
    await download_video_exemplar.edit_photo_safely(
        message_id=user_data.get("message_id"),
        text=SendMessagesUser.send_video_data(user_data.get("language")).format(
            title=download_video_exemplar.title,
            loading_bar=""
        ),
        photo=download_video_exemplar.photo)
    await download_video_exemplar.edit_reply_markup_safely(
        message_id=user_data.get('message_id'),
        reply_markup=user_keyboards.start(
            quality=download_video_exemplar.video_quality,
            url=download_video_exemplar.video_id,
            language=user_data.get('language')
        )
    )


@router.callback_query(lambda call: call.data.split(' ')[0] == "download_image")
async def download_image(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    url = f"https://www.youtube.com/watch?v={data[-1]}"
    user_data = await state.get_data()
    download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state, url=url)
    image = types.URLInputFile(download_video_exemplar.photo)
    await call.message.answer_photo(
        photo=image,
        # reply_markup=user_keyboards.back_to_main(
        #         user_data.get("language"),
        #         user_data.get("message_id"),
        #         data[-1]
        # )
    )
    await CheckAdsForDownload(call.message.chat.id)


@router.callback_query(lambda call: call.data.split(' ')[0] == "follow_channel")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    data = call.data.split(' ')
    download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state,
                                                      url=f"https://www.youtube.com/watch?v={data[-1]}")
    sub_data = db.Subs_class.get(download_video_exemplar.channel_id, call.from_user.id)

    if not sub_data:
        last_video_in_channel = download_video_exemplar.get_last_video_by_channel_id()
        if data[-1] != last_video_in_channel:
            download_video_exemplar = NewYoutubeDownloadClass(
                f"https://www.youtube.com/watch?v={last_video_in_channel}")
            await call.message.answer_photo(
                photo=types.URLInputFile(download_video_exemplar.photo),
                reply_markup=user_keyboards.start(
                    quality=download_video_exemplar.video_quality,
                    url=download_video_exemplar.video_id,
                    language=state_data.get("language")),
                caption=download_video_exemplar.title
            )
        db.Subs_class.add(
            user_id=call.from_user.id,
            notif=True,
            channel_id=download_video_exemplar.channel_id,
            last_publish_video_id=download_video_exemplar.video_id
        )
        await bot.send_message(call.from_user.id, SendMessagesUser.channel_add(state_data['language']))
    else:
        await bot.send_message(call.from_user.id, SendMessagesUser.channel_added(state_data['language']))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Youtube_follow_notif")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    data = call.data.split(' ')
    notif = False if data[2] == 'True' else True
    db.Subs_class.update_by_id(data[1], call.message.chat.id, notif=notif)
    await call.message.edit_reply_markup(inline_message_id=call.inline_message_id,
                                         reply_markup=user_keyboards.follow(
                                             int(data[3]),
                                             data[1],
                                             notif,
                                             state_data['language']
                                         ))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Youtube_follow_next")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    state_data = await state.get_data()
    data = call.data.split(' ')

    channels = db.Subs_class.get_channel_by_user_id(call.message.chat.id)
    index = 0 if int(data[1]) == len(channels) else int(data[1])

    info = get_channel_info(channel_id=channels[index].get('channel_id'))
    new_photo = types.InputMediaPhoto(media=types.URLInputFile(info.get('photo')))
    await bot.edit_message_media(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        media=new_photo
    )

    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=user_keyboards.follow(
                                            index=index, notif=channels[index].get('notif'),
                                            channel_id=channels[index].get('channel_id'),
                                            language=state_data['language']))


@router.callback_query(lambda call: call.data.split(' ')[0] == "Youtube_follow_delete")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    db.Subs_class.delete_by_id(data[1], call.from_user.id)


@router.callback_query(lambda call: call.data.split(' ')[0] == "search_list")
async def follow_channel(call: types.CallbackQuery, state: FSMContext):
    logger_bot.info(user_id=call.from_user.id, message=f"USER CLICK ON {call.data}")

    data = call.data.split(' ')
    user_data = await state.get_data()
    if data[1] == 'download':
        download_video_exemplar = NewYoutubeDownloadClass(chat_id=call.from_user.id, state=state, url=data[-1])
        message = await call.message.answer_photo(
            reply_markup=user_keyboards.start(
                quality=download_video_exemplar.video_quality,
                url=download_video_exemplar.video_id,
                language=user_data.get('language')),
            photo=types.URLInputFile(download_video_exemplar.photo),
            caption=SendMessagesUser.send_video_data(user_data.get("language")).format(
                title=download_video_exemplar.title + "\n", loading_bar="")
        )
        await state.update_data({"message_id": message.message_id})
    elif data[-1] != 'none':
        page = int(data[-1])
        try:
            if page == 1 and data[-3] == "next":
                videos = await search_list_in_youtube(page, data[-2])
                message = await bot.edit_message_reply_markup(
                    reply_markup=user_keyboards.search_list(videos, 2, 2, data[-2]),
                    message_id=user_data.get('message_id'), chat_id=call.message.chat.id)
                await state.update_data({"message_id": message.message_id})

            elif page == 2 and data[-3] == "back":
                videos = await search_list_in_youtube(page, data[-2])
                message = await bot.edit_message_reply_markup(
                    reply_markup=user_keyboards.search_list(videos, 1, 2, data[-2]),
                    message_id=user_data.get('message_id'), chat_id=call.message.chat.id)
                await state.update_data({"message_id": message.message_id})

        except Exception as err:
            await call.message.delete()
            videos = await search_list_in_youtube(1, data[-2])
            message = await call.message.answer(data[-2],
                                                reply_markup=user_keyboards.search_list(videos, 1, 2, data[-2]))
            await state.update_data({"message_id": message.message_id})
