from consts import *


class DownloadClass:
    def __init__(self, chat_id, state: FSMContext):
        self.editing_in_progress_message = False
        self.editing_in_progress_photo = False
        self.editing_in_progress_markup = False
        self.is_loading_proces_send = False
        self.list_loading_download = ["□□□□□□□□", "■□□□□□□□", "■■□□□□□□", "■■■□□□□□", "■■■■□□□□", "■■■■■□□□",
                                      "■■■■■■□□", "■■■■■■■□", "■■■■■■■□", "■■■■■■■■"]
        self.list_loading_sending = ["■□□□□", "■■□□□", "■■■□□", "■■■■□", "■■■■■", "■■■■□", "■■■□□", "■■□□□", "■□□□□"]
        self.is_loading_now = True
        self.chat_id = chat_id
        self.state = state

    async def edit_message_safely(self, message_id, text, reply_markup=None):
        if self.editing_in_progress_message:
            return
        try:
            self.editing_in_progress_message = True
            await bot.edit_message_text(chat_id=self.chat_id,
                                        message_id=message_id,
                                        text=text,
                                        reply_markup=reply_markup)
        except Exception as err:
            pass
        finally:
            self.editing_in_progress_message = False

    async def edit_photo_safely(self, message_id, text, photo):
        if self.editing_in_progress_photo:
            return
        try:
            await bot.edit_message_media(
                chat_id=self.chat_id,
                message_id=message_id,
                media=aiogram_types.InputMediaPhoto(
                    media=aiogram_types.URLInputFile(photo),
                    caption=text),
            )
        except as_exceptions.TelegramBadRequest:
            pass
        finally:
            self.editing_in_progress_photo = False

    async def edit_reply_markup_safely(self, message_id, reply_markup=None):
        if self.editing_in_progress_markup:
            return
        try:
            self.editing_in_progress_markup = True
            await bot.edit_message_reply_markup(
                chat_id=self.chat_id,
                message_id=message_id,
                reply_markup=reply_markup)
        except Exception as err:
            pass
        finally:
            self.editing_in_progress_markup = False

    async def send_video_file(self, chat_id, file_path, message='', width=430, height=932, reply_markup=None, supports_streaming=False):
        item = 0
        while item <= 5:
            try:
                message = await bot.send_video(
                    chat_id=chat_id,
                    request_timeout=1000000,
                    video=aiogram_types.FSInputFile(file_path),
                    caption=message,
                    parse_mode=ParseMode.HTML,
                    width=width,
                    height=height,
                    reply_markup=reply_markup,
                    supports_streaming=supports_streaming
                )
                self.is_loading_proces_send = False
                return message
            except Exception:
                item += 1
        self.is_loading_proces_send = False
        return "ERROR"

    async def send_video_buffer(self):
        user_data = await self.state.get_data()
        print(user_data.get("language"))

    async def send_audio_file(self, chat_id, file_path, message='', reply_markup=None, thumbnail=None, filename=None):
        item = 0
        while item <= 5:
            try:
                message = await bot.send_audio(
                    chat_id=chat_id,
                    thumbnail=thumbnail,
                    request_timeout=1000000,
                    audio=aiogram_types.FSInputFile(path=file_path, filename=filename),
                    caption=message,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
                self.is_loading_proces_send = False
                return message
            except Exception:
                item += 1

    async def send_audio_buffer(self):
        pass
