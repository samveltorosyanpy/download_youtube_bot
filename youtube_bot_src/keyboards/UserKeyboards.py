from aiogram import types
from youtube_bot_src.services.texts.send_message_texts import SendKeyboardsName
from consts import *


class InlineUserKeyboards:
    def start(self, quality, url, language):
        quality_key = []

        for qua in sorted(quality, key=lambda x: int(x[:-1])):
            if int(qua[:-1]) >= 1080:
                qua = qua + ' ⚡️'
            else:
                qua = qua + ' 📹'
            quality_key.append(types.InlineKeyboardButton(text=qua, callback_data=f"download_video {qua} {url}"))

        key_list = [quality_key[i:i + 3] for i in range(0, len(quality_key), 3)]
        key_list.insert(0, [
            types.InlineKeyboardButton(text=SendKeyboardsName.music(language), url=f'https://t.me/sy_mus')
        ])
        key_list.insert(1, [
            types.InlineKeyboardButton(text=SendKeyboardsName.start(language)[1],callback_data=f'follow_channel {url}')
        ])
        key_list.append(
            [types.InlineKeyboardButton(text='mp3 🎧', callback_data=f'download_mp3 {url}'),
             types.InlineKeyboardButton(text='🖼', callback_data=f'download_image {url}')
             ])
        key_list.append(
            [types.InlineKeyboardButton(text=SendKeyboardsName.start(language)[0], url='https://t.me/BaitCons')])

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def download_tiktok_audio(self, vid_id):
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="MP3 🎧",
                callback_data=f'download_tiktok_mp3 {vid_id}')]
        ])
    def back_to_main(self, language, message_id, video_id):
        key_list = [[
            types.InlineKeyboardButton(text=SendKeyboardsName.back_to_main(language), callback_data=f'back_to_main {message_id} {video_id}')
        ]]
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)
    def create_keyboard_ads(self, but):
        key_list = []
        for text in but:
            key_list.append([types.InlineKeyboardButton(text=text, url=but[text])])
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def edit_mp3(self, language):
        key_list = [[
            types.InlineKeyboardButton(text=SendKeyboardsName.edit_mp3(language), callback_data=f'Effect_edit')
        ]]
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def audio_edit_buttons(self, language):
        text_list = SendKeyboardsName.audio_edit_buttons(language)

        key_list = [
            [types.InlineKeyboardButton(text=text_list[0], callback_data=f'Effect_help')],
            [
                types.InlineKeyboardButton(text=text_list[1], callback_data=f'Effect_reverb'),
                types.InlineKeyboardButton(text=text_list[2], callback_data=f'Effect_8d')
            ],
            [types.InlineKeyboardButton(text=text_list[3], callback_data=f'Effect_bass')],
            [types.InlineKeyboardButton(text=text_list[4], callback_data=f'Effect_pitch')],
            [types.InlineKeyboardButton(text=text_list[5], callback_data=f'Effect_speed')],
            [types.InlineKeyboardButton(text=text_list[6], callback_data=f'Effect_confirm')],
        ]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def audio_help_back(self, language):
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=SendKeyboardsName.back(language), callback_data=f'Effect_back')]
        ])

    def audio_edit_effects(self, arr, effect, language):
        key_list = [
            [types.InlineKeyboardButton(text='🚫', callback_data=f'Effect_add 0 {effect}')],
            [types.InlineKeyboardButton(text=SendKeyboardsName.back(language),
                                        callback_data=f'Effect_back')],
        ]

        for i in arr:
            key_list[0].append(
                types.InlineKeyboardButton(text=str(i), callback_data=f'Effect_add {i} {effect}'))

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def follow(self, index, channel_id, notif, language):
        not_em = '🔔' if notif is True else '🔕'
        text_list = SendKeyboardsName.follow(language)
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=f'{text_list[0]} {not_em}',
                                           callback_data=f'Youtube_follow_notif {channel_id} {notif} {index + 1}'),
                types.InlineKeyboardButton(text=text_list[1], callback_data=f'Youtube_follow_delete {channel_id}'),
                types.InlineKeyboardButton(text=text_list[2], callback_data=f'Youtube_follow_next {index + 1}')
            ]
        ])

    def langusage(self):
        key_list = [[types.InlineKeyboardButton(text='Հայերեն 🇦🇲', callback_data=f'change_language hy Հայերեն')],
                    [types.InlineKeyboardButton(text='English 🇺🇸', callback_data=f'change_language en English')],
                    [types.InlineKeyboardButton(text='русский 🇷🇺', callback_data=f'change_language ru русский')]]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def langusage_new(self):
        key_list = [[types.InlineKeyboardButton(text='Հայերեն 🇦🇲', callback_data=f'change_language_new hy Հայերեն')],
                    [types.InlineKeyboardButton(text='English 🇺🇸', callback_data=f'change_language_new en English')],
                    [types.InlineKeyboardButton(text='русский 🇷🇺', callback_data=f'change_language_new ru русский')]]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def channel(self):
        key_list = [[types.InlineKeyboardButton(text='присоединиться к каналу ✅', url="https://t.me/BaitCons")]]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    def search_list(self, data, page, max_page, text):
        key_list = []
        for r in data:
            key_list.append([types.InlineKeyboardButton(
                text=r['name'],
                callback_data=f"search_list download {r['url']}")]
            )

        key_list.append(
            [types.InlineKeyboardButton(text="<", callback_data=f'search_list back {text} {page}'),
             types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data=f'search_list none'),
             types.InlineKeyboardButton(text=">", callback_data=f'search_list next {text} {page}')]
        )
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)


class ReplyUserKeyboard:
    @staticmethod
    def main():
        key_list = [[types.KeyboardButton(text="🔎 search"),
                     types.KeyboardButton(text="👤 subs"),
                     types.KeyboardButton(text="🏳️ language")]]

        return types.ReplyKeyboardMarkup(keyboard=key_list, resize_keyboard=True)

    @staticmethod
    def help(name):
        key_list = [[types.InlineKeyboardButton(text=name, url="https://t.me/sy_info")]]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)
