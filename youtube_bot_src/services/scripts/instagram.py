import time

import requests, asyncio
from consts import *
import subprocess
from aiogram import types
import mimetypes
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums.parse_mode import ParseMode

class InstagramClass:
    def __init__(self, url, user_id, message_id):
        self.user_list = [
            {
                "login": "esga_ra",
                "password": "EdgarLrjikyan055"
            },
            # {
            #     "login": "1_sam___",
            #     "password": "Administratore0*"
            # },
        ]
        self.message_id = message_id
        self.url = url
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "X-CSRFToken": self.session.get("https://www.instagram.com/").cookies["csrftoken"],
        }
        self.user_id = user_id
        self.list_loading = ["■□□□□", "■■□□□", "■■■□□", "■■■■□", "■■■■■", "■■■■□", "■■■□□", "■■□□□"]
        self.close_loop = False
        self.editing_in_progress = False

    async def edit_message_safely(self, text, reply_markup=None):
        if self.editing_in_progress:
            return
        try:
            self.editing_in_progress = True
            await bot.edit_message_text(chat_id=self.user_id, message_id=self.message_id, text=text, reply_markup=reply_markup)
        except Exception as err:
            logger_bot.error(err)
        finally:
            self.editing_in_progress = False

    async def loading_download_message(self, text):
        i = 0
        while self.close_loop is False:
            i = 0 if i == len(self.list_loading) else i
            message = f"{text} {self.list_loading[i]}"
            await self.edit_message_safely(message)
            i += 1
            await asyncio.sleep(0.3)
        else:
            await bot.delete_message(chat_id=self.user_id, message_id=self.message_id)
            await bot.delete_message(chat_id=self.user_id, message_id=self.message_id-1)



    async def authorization(self):
        for user in self.user_list:
            login_data = {
                "username": user["login"],
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{user['password']}",
                "queryParams": {},
                "optIntoOneTap": "false",
            }

            response = self.session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data,
                headers=self.headers,
                allow_redirects=True,
            )
            try:
                if response.status_code == 200 and response.json().get("authenticated"):
                    logger_bot.info("[+] Успешная авторизация!")

                    with open("cookies.txt", "w") as f:
                        for cookie in self.session.cookies:
                            if cookie.name == "sessionid":
                                f.write(f"{cookie.domain}\tTRUE\t/\tFALSE\t{cookie.expires}\t{cookie.name}\t{cookie.value}\n")
                                return
                    logger_bot.info("[+] Cookies сохранены в 'cookies.txt'")
                else:
                    logger_bot.info("[-] Ошибка авторизации")
            except Exception:
                pass

    async def download(self):
        command = f'gallery-dl --sleep 5 -C cookies.txt "{self.url}"'
        item = 1
        status_code = 200

        while item <= 2:
            logger_bot.info(f"porcum em qashel {item}")
            req = self.session.get(url=self.url, headers=self.headers)
            if req.status_code != 200:
                print(f"url status code {req.status_code}")
                item += 1
                await asyncio.sleep(4)
                continue

            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)

            if len(execute.stderr.read().decode()) > 0:
                print(f"ERROR: {execute.stderr.read().decode()}")
                await self.authorization()
                item += 1
                status_code = 1404
                await asyncio.sleep(4)
                continue

            result = execute.stdout.read() or ' '.encode()
            result = result.decode()
            rows = []
            for row in result.split("#"):
                if row == "\n" or row == '' or row == ' ':
                    continue
                row = row.replace("\n", "").replace(" ", "").replace("./", f"{PATH}/")
                rows.append(row)
            if len(rows) == 1:
                try:
                    if rows[0][-3:] == "mp4":
                        await bot.send_video(chat_id=self.user_id, video=types.FSInputFile(rows[0]), request_timeout=100000,
                                             width=430, height=932, parse_mode=ParseMode.HTML)
                    elif mimetypes.guess_type(rows[0])[0].startswith("image"):
                        await bot.send_photo(chat_id=self.user_id, photo=types.FSInputFile(rows[0]))
                except Exception:
                    continue
            elif len(rows) > 1:
                media_group = MediaGroupBuilder()
                for row in rows:
                    try:
                        if row[-3:] == "mp4":
                            media_group.add(type="video", media=types.FSInputFile(row))
                        elif row[-4:] in [".jpg"]:
                            media_group.add(type="photo", media=types.FSInputFile(row))
                    except Exception:
                        continue
                await bot.send_media_group(chat_id=self.user_id, media=media_group.build())
            item = 3

        self.close_loop = True
        return status_code
