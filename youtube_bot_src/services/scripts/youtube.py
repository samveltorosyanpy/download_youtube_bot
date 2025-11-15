import scrapetube
import aiofiles
import datetime
from youtubesearchpython import Video
from pytube import extract, YouTube
from consts import *
import requests
from openai import OpenAI
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from youtube_bot_src.services.db import Users_class
from youtube_bot_src.keyboards import user_keyboards
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
import io
import aiohttp, asyncio
from aiogram import exceptions

from youtubesearchpython import VideosSearch

editing_in_progress = False


async def search_list_in_youtube(page, text):
    try:
        youtube_search = VideosSearch(text, limit=16)
        videos = []
        count = 0 if page == 1 else 8
        for i in youtube_search.result()['result'][count:]:
            videos.append({
                "name": i.get('title'),
                "url": f"https://www.youtube.com/watch?v={i.get('id')}"
            })
            count += 1
            if count == 8 or count == 16:
                break
    except TypeError:
        return None
    return videos


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


class ClassYoutube:
    def __init__(self, url):
        self.video_id = extract.video_id(url)
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.yt = YouTube(url=url)
        video_info = Video.getInfo(self.url)
        self.channel_id = video_info['channel'].get('id')
        self.publish_date = video_info.get('publishDate')
        self.photo = video_info.get('thumbnails')[-1].get("url")
        self.title = video_info.get('title')
        self.video_quality = ["1080p", "720p", "480p", "360p", "144p"]
        self.list_loading = ["■□□□□", "■■□□□", "■■■□□", "■■■■□", "■■■■■", "■■■■□", "■■■□□", "■■□□□", "■□□□□"]
        self.file = bytearray()

    async def send_video(self, filename, user_id, language, download_msg):
        await bot.send_video(chat_id=user_id, request_timeout=100000,
                             video=types.FSInputFile(filename),
                             caption=SendMessagesUser.send_video(
                                 language) + download_msg,
                             width=1280, height=720, parse_mode=ParseMode.HTML)
        await asyncio.sleep(3)

    async def send_audio(self, user_id, language):
        send_status = 0
        while send_status < 5:
            try:
                await bot.send_audio(
                    chat_id=user_id, request_timeout=100000, title=self.title,
                    thumbnail=types.FSInputFile(f"{PATH}/media/bot/logo.jpg"),
                    audio=types.input_file.BufferedInputFile(self.file, filename="Video-Mp3.mp3"),
                    caption=SendMessagesUser.send_audio(language=language),
                    reply_markup=user_keyboards.edit_mp3(language=language),
                    parse_mode=ParseMode.HTML)
                send_status = 5
                await asyncio.sleep(3)
            except Exception as err:
                logger_bot.error(user_id=user_id, message=f"In send audio {err}")
                send_status += 1

    async def send_message_loading(self, call, download_processing, file_total_size, file_size, quality_m, message_id,
                                   language):
        msgs = SendMessagesUser.download_process(language, type_d="video")
        try:
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"{msgs[0]} {self.list_loading[download_processing]} {file_total_size + file_size} {msgs[1]} {quality_m}",
                message_id=message_id
            )
        except exceptions.TelegramBadRequest as err:
            logger_bot.error(user_id=call.from_user.id, message=err)
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"{msgs[0]} {self.list_loading[download_processing + 1]} {file_total_size + file_size} {msgs[1]} {quality_m}",
                message_id=message_id
            )
        except exceptions.TelegramRetryAfter as err:
            logger_bot.error(user_id=call.from_user.id, message=err)
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                text=f"{msgs[0]} {self.list_loading[download_processing + 1]} {file_total_size + file_size} {msgs[1]} {quality_m}",
                message_id=message_id
            )

    async def Download_video(self, url, quality, call, language, message_id, quality_m, photo):
        download_processing = 0
        file_total_size = 0
        time = datetime.datetime.now().second
        msgs = SendMessagesUser.download_process(language, type_d="video")
        logger_bot.info(user_id=call.from_user.id, message=url)

        json = {'url': url, "vQuality": quality}
        User_Agents = [
            'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0.',
            'My User Agent 1.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            "python-requests/2.28.2",
        ]
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)
        filename = f"{PATH}/media/videos/{self.video_id}_{datetime.datetime.now().microsecond}.mp4"
        for user_agent in User_Agents:
            with requests.post(url=COBALT_API, json=json, headers=headers) as r:
                state = False
                logger_bot.info(user_id=call.from_user.id, message=r.status_code)

                try:
                    headers['User-Agent'] = user_agent
                    print(r.json())
                    video_url = r.json()["url"]
                    if r.status_code != 200:
                        continue
                    else:
                        state = True
                        break
                except Exception:
                    continue

        if state:
            async with aiofiles.open(filename, mode='wb') as file:
                download_session = await aiohttp.ClientSession(timeout=session_timeout, headers=headers).get(video_url)
                while True:
                    chunk = await download_session.content.read(32 * 1024)
                    file_size = int(len(self.file) / 1000000)

                    if datetime.datetime.now().second == 0:
                        time = 0
                    if time < datetime.datetime.now().second:
                        time = datetime.datetime.now().second
                        if download_processing == 9:
                            download_processing = 0

                        await edit_message_safely(chat_id=call.from_user.id,
                                                  text=f"{msgs[0]} {self.list_loading[download_processing]} {file_total_size + file_size} {msgs[1]} {quality_m}",
                                                  message_id=message_id)

                        download_processing += 1

                    if not chunk:
                        await file.write(self.file)
                        logger_bot.info(user_id=call.from_user.id, message=[datetime.datetime.now(), "finish download"])

                        await bot.edit_message_text(chat_id=call.from_user.id, text=msgs[2],
                                                    message_id=message_id)

                        await asyncio.gather(self.send_video(
                            download_msg=f"\n{msgs[0]} ■■■■■ {file_total_size + file_size} {msgs[1]} {quality_m}",
                            filename=filename,
                            user_id=call.from_user.id,
                            language=language
                        ))

                        await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
                        Users_class.update_by_id(user_id=call.from_user.id, is_dead=False)

                        logger_bot.info(user_id=call.from_user.id, message=[datetime.datetime.now(), "finish sending"])
                        break

                    if file_size > 1000:
                        await file.write(self.file)
                        file_total_size += file_size
                        self.file = bytearray()
                    else:
                        self.file.extend(chunk)
        else:
            # logger_bot.info([r.json(), url])
            await call.message.answer_photo(
                photo=types.URLInputFile(photo),
                caption=SendMessagesUser.send_video_data(SendMessagesUser.send_video_region_error(language))
            )
            await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
            return
        try:
            # pass
            os.remove(filename)
        except FileNotFoundError:
            pass
        except FileExistsError:
            pass

    async def Download_audio(self, url, call, language, message_id):
        download_processing = 0
        time = datetime.datetime.now().second
        msgs = SendMessagesUser.download_process(language, type_d="audio")
        json = {'url': url, "isAudioOnly": True}
        User_Agents = [
            'My User Agent 1.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
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
                logger_bot.info(user_id=call.from_user.id, message=r.status_code)

                try:
                    headers['User-Agent'] = user_agent
                    video_url = r.json()["url"]
                    if r.status_code != 200:
                        continue
                    else:
                        state = True
                        break
                except Exception:
                    continue
        download_session = await aiohttp.ClientSession(timeout=session_timeout, headers=headers).get(video_url)
        if state:
            while True:
                chunk = await download_session.content.read(16 * 1024)
                file_size = int(len(self.file) / 1000000)

                if datetime.datetime.now().second == 0:
                    time = 0
                if time < datetime.datetime.now().second:
                    time = datetime.datetime.now().second
                    if download_processing == 9:
                        download_processing = 0

                    await edit_message_safely(chat_id=call.from_user.id,
                                              text=f"{msgs[0]} {self.list_loading[download_processing]} {0 + file_size} {msgs[1]}",
                                              message_id=message_id)

                    download_processing += 1

                if not chunk:
                    logger_bot.info(user_id=call.from_user.id, message=[datetime.datetime.now(), "finish download"])
                    await bot.edit_message_text(chat_id=call.from_user.id, text=msgs[2],
                                                message_id=message_id)

                    await asyncio.gather(self.send_audio(
                        user_id=call.from_user.id,
                        language=language
                    ))

                    await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
                    Users_class.update_by_id(user_id=call.from_user.id, is_dead=False)

                    logger_bot.info(user_id=call.from_user.id, message=[datetime.datetime.now(), "finish sending"])
                    break
                self.file.extend(chunk)

    async def get_transcription(self, url, call, language, message_id):
        os.environ["OPENAI_API_KEY"] = OPENAI_KEY
        msgs = SendMessagesUser.download_process(language, type_d="text")
        download_processing = 2
        time = datetime.datetime.now().second
        json = {'url': url, "isAudioOnly": True}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)

        await bot.edit_message_text(chat_id=call.from_user.id, text=f"{msgs[0]} ■□□□□ 0 {msgs[1]}",
                                    message_id=message_id)

        with requests.post(url=COBALT_API, json=json, headers=headers) as r:
            video_url = r.json()["url"]

        download_session = await aiohttp.ClientSession(timeout=session_timeout, headers=headers).get(video_url)
        while True:
            chunk = await download_session.content.read(10 * 1024)
            file_size = int(len(self.file) / 1000000)
            if datetime.datetime.now().second == 0:
                time = 0
            if time < datetime.datetime.now().second:
                time = datetime.datetime.now().second
                if download_processing == 9:
                    download_processing = 0

                await asyncio.gather(self.send_message_loading(call=call, download_processing=download_processing,
                                                               file_total_size=0, file_size=file_size,
                                                               quality_m=" ", message_id=message_id, language=language))

                download_processing += 1

            if not chunk:
                await bot.edit_message_text(chat_id=call.from_user.id, text=msgs[2],
                                            message_id=message_id)
                audio_io = io.BytesIO(self.file)
                audio_io.name = "audio.mp3"

                client = OpenAI()
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_io
                )
                logger_bot.info(type(transcript))
                await call.message.answer(transcript.text.lower())

                await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
                logger_bot.info([datetime.datetime.now(), "finish sending"])
                break

            self.file.extend(chunk)

        download_session.close()
        logger_bot.info(download_session.closed)


def get_last_video_by_channel_id(channel_id):
    videos = scrapetube.get_channel(channel_id)
    for video in videos:
        return video['videoId']

