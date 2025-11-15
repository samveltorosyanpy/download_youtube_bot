from consts import *
import requests
from datetime import datetime
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
import aiohttp, asyncio, aiofiles
from youtube_bot_src.services.db import Users_class
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from youtube_bot_src.keyboards import user_keyboards

editing_in_progress = False


async def edit_message_safely(chat_id, message_id, text, reply_markup=None):
    global editing_in_progress

    if editing_in_progress:
        return

    try:
        editing_in_progress = True
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)
    except Exception as err:
        logger_bot.error(err)
    finally:
        editing_in_progress = False


class ClassTikTok:
    def __init__(self, url):
        self.url = url
        self.list_loading = ["■□□□□", "■■□□□", "■■■□□", "■■■■□", "■■■■■", "■■■■□", "■■■□□", "■■□□□", "■□□□□"]
        self.file = bytearray()

    async def send_video(self, filename, user_id, language, download_msg):
        TikTok_videos.append(self.url)
        vid_id = TikTok_videos.index(self.url)
        await bot.send_video(chat_id=user_id, request_timeout=100000,
                             video=types.FSInputFile(filename),
                             caption=SendMessagesUser.send_video(
                                 language) + download_msg,
                             width=430, height=932, parse_mode=ParseMode.HTML,
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                 [types.InlineKeyboardButton(
                                     text="MP3 🎧",
                                     callback_data=f'download_tiktok_mp3 {vid_id}')]
                             ]))
        await asyncio.sleep(1)
        return

    async def send_audio(self, user_id, language):
        send_status = 0
        while send_status < 5:
            try:
                await bot.send_audio(
                    chat_id=user_id, request_timeout=100000,
                    thumbnail=types.FSInputFile(f"{PATH}/media/bot/TikTokLogo.jpg"),
                    audio=types.input_file.BufferedInputFile(self.file, filename="Video-Mp3.mp3"),
                    caption=SendMessagesUser.send_audio(language=language),
                    reply_markup=user_keyboards.edit_mp3(language=language),
                    parse_mode=ParseMode.HTML
                )
                send_status = 5
                await asyncio.sleep(3)
            except Exception as err:
                logger_bot.error(user_id=user_id, message=f"In send audio {err}")
                send_status += 1

    async def download_video(self, language, msg, message_id):
        download_processing = 0
        file_total_size = 0
        time = datetime.now().second
        msgs = SendMessagesUser.download_process(language, type_d="video")
        logger_bot.info(user_id=msg.from_user.id, message=self.url)
        json = {"vQuality": "720p", 'url': self.url}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        User_Agents = [
            'My User Agent 1.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            "python-requests/2.28.2"
        ]
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)
        filename = f"{PATH}/media/videos/{datetime.now()}.mp4"
        for user_agent in User_Agents:
            with requests.post(url=COBALT_API, json=json, headers=headers) as r:
                state = False
                logger_bot.info(r.status_code)
                try:
                    headers['User-Agent'] = user_agent
                    video_url = r.json()["url"]
                    if r.status_code == 200:
                        state = True
                        break
                    else:
                        continue
                except Exception:
                    continue

        if state:
            async with aiofiles.open(filename, mode='wb') as file:
                download_session = await aiohttp.ClientSession(timeout=session_timeout, headers=headers).get(video_url)
                while True:
                    chunk = await download_session.content.read(32 * 1024)
                    file_size = int(len(self.file) / 1000000)

                    if datetime.now().second == 0:
                        time = 0
                    if time < datetime.now().second:
                        time = datetime.now().second
                        if download_processing == 9:
                            download_processing = 0

                        await edit_message_safely(chat_id=msg.from_user.id,
                                                  text=f"{msgs[0]} {self.list_loading[download_processing]} {file_total_size + file_size} {msgs[1]}",
                                                  message_id=message_id)

                        download_processing += 1

                    if not chunk:
                        await file.write(self.file)
                        logger_bot.info([datetime.now(), "finish download"])

                        await bot.edit_message_text(chat_id=msg.from_user.id, text=msgs[2],
                                                    message_id=message_id)

                        await asyncio.gather(self.send_video(
                            download_msg=f"\n{msgs[0]} ■■■■■ {file_total_size + file_size} {msgs[1]}",
                            filename=filename,
                            user_id=msg.from_user.id,
                            language=language
                        ))

                        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
                        Users_class.update_by_id(user_id=msg.from_user.id, is_dead=False)

                        logger_bot.info([datetime.now(), "finish sending"])
                        break

                    if file_size > 1000:
                        await file.write(self.file)
                        file_total_size += file_size
                        self.file = bytearray()
                    else:
                        self.file.extend(chunk)
        else:
            logger_bot.info([r.json(), self.url])
            return
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        except FileExistsError:
            pass

    async def download_audio(self, call: types.CallbackQuery, language, message_id):
        download_processing = 0
        time = datetime.now().second
        msgs = SendMessagesUser.download_process(language, type_d="audio")
        json = {'url': self.url, "isAudioOnly": True}
        User_Agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'My User Agent 1.0',
            'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            "python-requests/2.28.2"
        ]
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)
        state = False
        for user_agent in User_Agents:
            with requests.post(url=COBALT_API, json=json, headers=headers) as r:
                state = False
                logger_bot.info(r.status_code)

                try:
                    headers['User-Agent'] = user_agent
                    video_url = r.json()["url"]
                    if r.status_code == 200:
                        state = True
                        break
                    else:
                        continue
                except Exception:
                    continue
        download_session = await aiohttp.ClientSession(timeout=session_timeout, headers=headers).get(video_url)
        if state:
            while True:
                chunk = await download_session.content.read(16 * 1024)
                file_size = int(len(self.file) / 1000000)

                if datetime.now().second == 0:
                    time = 0
                if time < datetime.now().second:
                    time = datetime.now().second
                    if download_processing == 9:
                        download_processing = 0

                    await edit_message_safely(chat_id=call.message.chat.id,
                                              text=f"{msgs[0]} {self.list_loading[download_processing]} {0 + file_size} {msgs[1]}",
                                              message_id=message_id)

                    download_processing += 1

                if not chunk:
                    logger_bot.info([datetime.now(), "finish download"])
                    await edit_message_safely(chat_id=call.message.chat.id,
                                              text=msgs[2],
                                              message_id=message_id)
                    await asyncio.gather(self.send_audio(
                        user_id=call.message.chat.id,
                        language=language
                    ))
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
                    Users_class.update_by_id(user_id=call.message.chat.id, is_dead=False)
                    logger_bot.info([datetime.now(), "finish sending"])
                    break
                self.file.extend(chunk)
