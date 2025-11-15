import time

import requests, asyncio
from consts import *
import subprocess
from aiogram import types
import mimetypes
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums.parse_mode import ParseMode
from youtube_bot_src.services.downloads.MainDownloadClass import DownloadClass

class InstagramDownloadClass(DownloadClass):
    def __init__(self, url, chat_id, state):
        super().__init__(chat_id=chat_id, state=state)
        self.url = url
        self.session = requests.Session()
        self.is_loading_proces_download = True
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "X-CSRFToken": self.session.get("https://www.instagram.com/").cookies["csrftoken"],
        }
        self.chat_id = chat_id
        self.close_loop = False
        self.editing_in_progress = False
        self.sending_index = 0
        self.error_back = 0
        self.files_path = []

    # async def edit_message_safely(self, text, reply_markup=None):
    #     if self.editing_in_progress:
    #         return
    #     try:
    #         self.editing_in_progress = True
    #         await bot.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text,
    #                                     reply_markup=reply_markup)
    #     except Exception as err:
    #         logger_bot.error(err)
    #     finally:
    #         self.editing_in_progress = False

    # async def loading_download_message(self, text):
    #     i = 0
    #     while self.close_loop is False:
    #         i = 0 if i == len(self.list_loading) else i
    #         message = f"{text} {self.list_loading[i]}"
    #         await self.edit_message_safely(message)
    #         i += 1
    #         await asyncio.sleep(0.3)
    #     else:
    #         await bot.delete_message(chat_id=self.chat_id, message_id=self.message_id)
    #         await bot.delete_message(chat_id=self.chat_id, message_id=self.message_id - 1)

    async def loading_download(self):

        while self.is_loading_proces_download:
            user_data = await self.state.get_data()
            t = SendMessagesUser.sending_loading(user_data.get("language"))

            if self.sending_index == len(self.list_loading_sending) - 1:
                self.sending_index = 0

            is_proces_send_text = f"{t[1]} {self.list_loading_sending[self.sending_index]}"
            self.sending_index += 1

            await self.edit_message_safely(
                message_id=user_data.get("message_id"),
                text=f"{is_proces_send_text}")
            await asyncio.sleep(.5)
        else:
            user_data = await self.state.get_data()
            await self.edit_message_safely(
                message_id=user_data.get("message_id"),
                text=" ")

    def authorization(self):
        user_list = [
            {
                "login": "1_sam___",
                "password": "Administratore0*"
            },
        ]

        for user in user_list:
            response = self.session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data={
                    "username": user["login"],
                    "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{user['password']}",
                    "queryParams": {},
                    "optIntoOneTap": "false",
                },
                headers=self.headers,
                allow_redirects=True,
            )
            # try:
            if response.status_code == 200 and response.json().get("authenticated"):
                logger_bot.info("[+] Успешная авторизация!")

                with open("cookies.txt", "w") as f:
                    for cookie in self.session.cookies:
                        if cookie.name == "sessionid":
                            row = f"{cookie.domain}\tTRUE\t/\tFALSE\t{cookie.expires}\t{cookie.name}\t{cookie.value}\n"
                            f.write(row)
                logger_bot.info("[+] Cookies сохранены в 'cookies.txt'")
                break
            else:
                logger_bot.info("[-] Ошибка авторизации")
            # except Exception:
            #     logger_bot.info("[-] Ошибка авторизации")

    # async def download(self):
    #     command = f'gallery-dl --sleep 5 -C cookies.txt "{self.url}"'
    #     item = 1
    #     status_code = 200
    #
    #     while item <= 2:
    #         logger_bot.info(f"porcum em qashel {item}")
    #         req = self.session.get(url=self.url, headers=self.headers)
    #         if req.status_code != 200:
    #             print(f"url status code {req.status_code}")
    #             item += 1
    #             await asyncio.sleep(4)
    #             continue
    #
    #         execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
    #                                    stderr=subprocess.PIPE,
    #                                    stdin=subprocess.PIPE)
    #
    #         if len(execute.stderr.read().decode()) > 0:
    #             print(f"ERROR: {execute.stderr.read().decode()}")
    #             await self.authorization()
    #             item += 1
    #             status_code = 1404
    #             await asyncio.sleep(4)
    #             continue
    #
    #         result = execute.stdout.read() or ' '.encode()
    #         result = result.decode()
    #         rows = []
    #         for row in result.split("#"):
    #             if row == "\n" or row == '' or row == ' ':
    #                 continue
    #             row = row.replace("\n", "").replace(" ", "").replace("./", f"{PATH}/")
    #             rows.append(row)
    #
    #         if len(rows) == 1:
    #             try:
    #                 if rows[0][-3:] == "mp4":
    #                     await bot.send_video(chat_id=self.chat_id, video=types.FSInputFile(rows[0]),
    #                                          request_timeout=100000,
    #                                          width=430, height=932, parse_mode=ParseMode.HTML)
    #                 elif mimetypes.guess_type(rows[0])[0].startswith("image"):
    #                     await bot.send_photo(chat_id=self.chat_id, photo=types.FSInputFile(rows[0]))
    #             except Exception:
    #                 continue
    #         elif len(rows) > 1:
    #             media_group = MediaGroupBuilder()
    #             for row in rows:
    #                 try:
    #                     if row[-3:] == "mp4":
    #                         media_group.add(type="video", media=types.FSInputFile(row))
    #                     elif row[-4:] in [".jpg"]:
    #                         media_group.add(type="photo", media=types.FSInputFile(row))
    #                 except Exception:
    #                     continue
    #             await bot.send_media_group(chat_id=self.chat_id, media=media_group.build())
    #         item = 3
    #
    #     self.close_loop = True
    #     return status_code

    async def download(self):
        while self.error_back <= 2:
            execute = subprocess.Popen(f'gallery-dl --sleep 5 -C cookies.txt "{self.url}"',
                                       shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)

            logger_bot.info(f"porcum em qashel {self.error_back}")
            req = self.session.get(url=self.url, headers=self.headers)
            if req.status_code != 200:
                print(f"url status code {req.status_code}")
                self.error_back += 1
                time.sleep(4)
                continue

            if len(execute.stderr.read().decode()) > 0:
                print(f"ERROR: {execute.stderr.read().decode()}")
                self.authorization()
                self.error_back += 1
                time.sleep(4)
                continue

            result = execute.stdout.read() or ' '.encode()
            result = result.decode()
            for row in result.split("#"):
                if row == "\n" or row == '' or row == ' ':
                    return
                print(row)
                row = row.replace("\n", "").replace(" ", "").replace("./", f"{PATH}/")
                self.files_path.append(row)



    async def download_video(self):
        self.sending_index = 1
        loop = asyncio.get_event_loop()
        loop.create_task(self.loading_download())
        loop.create_task(self.download())
        if len(self.files_path) == 1:
            # try:
            if self.files_path[0][-3:] == "mp4":
                await bot.send_video(chat_id=self.chat_id, video=types.FSInputFile(self.files_path[0]),
                                     request_timeout=100000,
                                     width=430, height=932, parse_mode=ParseMode.HTML)
            elif mimetypes.guess_type(self.files_path[0])[0].startswith("image"):
                await bot.send_photo(chat_id=self.chat_id, photo=types.FSInputFile(self.files_path[0]))
            # except Exception:
            #     continue
        elif len(self.files_path) > 1:
            media_group = MediaGroupBuilder()
            for row in self.files_path:
                # try:
                if row[-3:] == "mp4":
                    media_group.add(type="video", media=types.FSInputFile(row))
                elif row[-4:] in [".jpg"]:
                    media_group.add(type="photo", media=types.FSInputFile(row))
                # except Exception:
                #     continue
            await bot.send_media_group(chat_id=self.chat_id, media=media_group.build())
        # self.is_loading_proces_download = False
