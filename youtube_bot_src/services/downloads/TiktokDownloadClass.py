from youtube_bot_src.services.downloads.MainDownloadClass import DownloadClass
from youtubesearchpython import VideosSearch
from pytube import extract
from youtube_bot_src.services.texts.send_message_texts import SendMessagesUser
from youtubesearchpython import Video
import yt_dlp
import scrapetube
from consts import *

class TiktokDownloadClass(DownloadClass):
    def __init__(self, url, chat_id=None, state: FSMContext=None):
        super().__init__(chat_id=chat_id, state=state)
        self.url = url
        self.downloaded = 0
        self.total_downloaded = 0
        self.total_size = 0
        self.sending_index = 0
        self.download_speed = ""
        self.file_path = ""
        self.is_loading_proces_download = True
        self.quality_info = {}
        self.get_data()

    def get_data(self):
        item = 0
        while item < 5:
            try:
                with yt_dlp.YoutubeDL({}) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    self.quality_info = {
                        'width': info["formats"][-1]['width'],
                        'height': info["formats"][-1]['height'],
                        'id': info["id"]
                    }
                    self.total_size = info["formats"][-1]["filesize"]
                    item = 5
            except Exception:
                item += 1

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
            await self.edit_message_safely(
                message_id=user_data.get("message_id"),
                text=f"{is_proces_send_text}")
            await asyncio.sleep(.5)
        else:
            user_data = await self.state.get_data()
            await self.edit_message_safely(
                message_id=user_data.get("message_id"),
                text=" ")

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
            logger_bot.info(self.url)
            ydl.download([self.url])

    async def download_video(self):
        self.file_path = f"{PATH}/media/videos/tiktok_videos/{self.quality_info['id']}.mp4"

        user_data = await self.state.get_data()
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': self.file_path,
            'quiet': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            "progress_hooks": [self.hook]
        }

        loop = asyncio.get_event_loop()
        loop.create_task(self.loading_download())
        if os.path.exists(self.file_path) is False:
            await asyncio.to_thread(self.download, ydl_opts)
        self.is_loading_proces_download = False
        self.is_loading_proces_send = True
        await asyncio.sleep(1)
        await self.send_video_file(
            chat_id=self.chat_id, file_path=self.file_path,
            width=self.quality_info['width'],
            height=self.quality_info['height'],
            message=f"{SendMessagesUser.send_video_tiktok(user_data.get('language'))}",
            reply_markup=user_keyboards.download_tiktok_audio(self.quality_info['id'])
        )
        download_now[self.chat_id] = False

    async def download_mp3(self):
        self.file_path = f"{PATH}/media/videos/youtube_videos/{self.quality_info['id']}.mp3"

        user_data = await self.state.get_data()
        ydl_opts = {
            'format': "bestaudio/best",
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
            filename="Video-Mp3.mp3")

        download_now[self.chat_id] = False
