import asyncio
import subprocess

from youtube_bot_src.services.downloads.MainDownloadClass import DownloadClass
from youtubesearchpython import VideosSearch
from pytube import extract
from youtubesearchpython import Video
import yt_dlp
import scrapetube
from consts import *


async def search_list_in_youtube(page, text):
    videos = []
    try:
        youtube_search = VideosSearch(text, limit=16)
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
        videos = []
    return videos


def get_channel_info(channel_id):
    channel_url = f"https://www.youtube.com/channel/{channel_id}"

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    return {
        "channel_follower_count": info["channel_follower_count"],
        "title": info["title"],
        "photo": info["thumbnails"][-1]["url"]
    }


def get_base_info_by_video_id_from_youtube(url):
    video_id = extract.video_id(url)
    url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = Video.getInfo(url)

    return {
        "title": video_info.get('title'),
        "thumbnails": video_info.get('thumbnails')[-1].get("url")
    }


class NewYoutubeDownloadClass(DownloadClass):
    def __init__(self, url, chat_id=None, state: FSMContext = None):
        super().__init__(chat_id=chat_id, state=state)
        self.url = url
        self.video_id = extract.video_id(url)
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.video_info = Video.getInfo(self.url)
        self.title = self.video_info.get('title')
        self.photo = self.video_info.get('thumbnails')[-1].get("url")
        self.video_quality = ["1080p", "720p", "480p", "360p", "144p"]
        self.channel_id = self.video_info['channel'].get('id')
        self.publish_date = self.video_info.get('publishDate')
        self.total_downloaded = 0
        self.sending_index = 0
        self.audio_size = 0
        self.downloaded = 0
        self.total_size = 0
        self.download_speed = ""
        self.file_path = ""
        self.is_loading_proces_download = True
        self.quality_info = {}
        self.get_data()

    def get_last_video_by_channel_id(self):
        videos = scrapetube.get_channel(self.channel_id)
        try:
            for video in videos:
                return video['videoId']
        except Exception:
            return None

    def get_data(self):
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            formats = info.get('formats', [])
            for row in formats:
                if row["format_id"] == "140":
                    self.audio_size = int(row["filesize"])
                    break

            for row in formats:
                if row["format_id"] in ["137", "136", "135", "134", "160"]:
                    self.quality_info[
                        row['format_note'][:-1]
                    ] = {
                        "format_id": f"{row['format_id']}+140",
                        "height": row["height"],
                        "width": row["width"],
                        "filesize": int(row["filesize"]) + self.audio_size,
                    }
            self.title = info["title"]

    async def loading_download(self):
        while self.is_loading_proces_download or self.is_loading_proces_send:
            user_data = await self.state.get_data()

            t = SendMessagesUser.sending_loading(user_data.get("language")) or self.is_loading_proces_send
            if self.is_loading_proces_download:
                pr = int(self.downloaded) * 100 / int(self.total_size)
                index = int(pr) // len(self.list_loading_download) if pr != 100 else -1
                is_proces_send_text = f"{t[0]} {self.list_loading_download[index]} {round(pr, 1)}% {self.download_speed}"
            elif self.is_loading_proces_send:
                if self.sending_index == len(self.list_loading_sending) - 1:
                    self.sending_index = 0
                is_proces_send_text = f"{t[1]} {self.list_loading_sending[self.sending_index]}"
                self.sending_index += 1
            else:
                break

            await self.edit_photo_safely(
                message_id=user_data.get("message_id"),
                text=SendMessagesUser.send_video_data_is_loading_now(user_data.get("language")).format(
                    title=self.title + "\n",
                    loading_bar=is_proces_send_text + "\n"
                ),
                photo=self.photo)
            await asyncio.sleep(.5)
        else:
            user_data = await self.state.get_data()
            await self.edit_photo_safely(
                message_id=user_data.get("message_id"),
                text=SendMessagesUser.send_video_data_is_loading_now(user_data.get("language")).format(
                    title=self.title,
                    loading_bar=""
                ),
                photo=self.photo)

    def hook(self, d):
        try:
            self.download_speed = d["_speed_str"]
            self.downloaded = self.total_downloaded + d["downloaded_bytes"]
            if 'finished' == d["status"]:
                self.total_downloaded = self.total_downloaded + d["downloaded_bytes"]
        except KeyError:
            self.is_loading_proces_download, self.is_loading_proces_send = False, True

    def download(self, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        if "mp4" in self.file_path:
            logger_bot.info(f"ssssssss {self.file_path, }")

            command = [
                'ffmpeg', '-i', self.file_path,
                '-c', 'copy', '-movflags', '+faststart',
                f"{self.file_path[:-4]}_ffmpeg.mp4"
            ]
            subprocess.run(command, check=True)

    async def download_video(self, quality):
        self.file_path = f"{PATH}/media/videos/youtube_videos/{self.video_id}-{quality}.mp4"
        try:
            self.total_size = self.quality_info[str(quality)]['filesize']
        except KeyError:
            quality = list(self.quality_info.keys())[-1]
            self.total_size = self.quality_info[quality]['filesize']

        user_data = await self.state.get_data()
        ydl_opts = {
            'format': self.quality_info[str(quality)]['format_id'],
            'outtmpl': self.file_path,
            "progress_hooks": [self.hook]
        }

        loop = asyncio.get_event_loop()
        loop.create_task(self.loading_download())
        if os.path.exists(self.file_path) is False:
            await asyncio.to_thread(self.download, ydl_opts)
        self.is_loading_proces_send, self.is_loading_proces_download = True, False
        await asyncio.sleep(1)

        await self.send_video_file(
            chat_id=self.chat_id,
            supports_streaming=True,
            file_path=f"{self.file_path[:-4]}_ffmpeg.mp4",
            width=self.quality_info[str(quality)]['width'],
            height=self.quality_info[str(quality)]['height'],
            message=f"{SendMessagesUser.send_video(user_data.get('language'))}",
            reply_markup=user_keyboards.back_to_main(
                user_data.get("language"),
                user_data.get("message_id"),
                self.video_id),
        )
        download_now[self.chat_id] = False
        download_turn.remove(f"{self.chat_id}_{self.url}")

    async def download_mp3(self):
        self.file_path = f"{PATH}/media/videos/youtube_videos/{self.video_id}.mp3"
        self.total_size = self.audio_size

        user_data = await self.state.get_data()
        ydl_opts = {
            'format': "140",
            'outtmpl': self.file_path,
            "progress_hooks": [self.hook]
        }

        loop = asyncio.get_event_loop()
        loop.create_task(self.loading_download())

        if os.path.exists(self.file_path) is False:
            await asyncio.to_thread(self.download, ydl_opts)

        self.is_loading_proces_download, self.is_loading_proces_send = False, True
        await asyncio.sleep(1)
        await self.send_audio_file(
            chat_id=self.chat_id, file_path=self.file_path,
            thumbnail=aiogram_types.FSInputFile(f"{PATH}/media/bot/logo.jpg"),
            message=f"{SendMessagesUser.send_audio(user_data.get('language'))}",
            reply_markup=user_keyboards.back_to_main(user_data.get("language"),
                                                     user_data.get("message_id"),
                                                     self.video_id),
            filename=f"{self.title}.mp3"
        )
        download_now[self.chat_id] = False

        # if os.path.exists(file_path):
        #     os.remove(file_path)
        # download_session = await aiohttp.ClientSession(
        #     timeout=self.session_timeout,
        #     headers=self.headers
        # ).get(self.download_url)
        # logger_bot.info(user_id=self.chat_id, message=f"Start download video: {self.url}")
        # print(self.json)
        # async with aiofiles.open(file_path, mode='wb') as file:
        #     while True:
        #         chunk = await download_session.content.read(1024)
        #         print(chunk)
        #         if not chunk:
        #             break
        #         self.file += chunk
        #     logger_bot.info(user_id=self.chat_id, message=f"finish download on path: {file_path}")
        #     await file.write(self.file)
