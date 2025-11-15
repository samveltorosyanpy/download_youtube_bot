from aiogram import types


class InlineAdminKeyboards:
    @staticmethod
    def main_functions():
        key_list = [[
            types.InlineKeyboardButton(text='✅ Рассылка', callback_data=f'mailing'),
            types.InlineKeyboardButton(text='💚 показ', callback_data='sharing')
        ],
            [
                types.InlineKeyboardButton(text='💹 подписка на канал', callback_data=f'subs_on_channel_ads'),
                types.InlineKeyboardButton(text='настройки', callback_data=f'settings')
            ],
            [
                types.InlineKeyboardButton(text='Статистика', callback_data=f'statistics'),
                types.InlineKeyboardButton(text='рекламы', callback_data=f'ads_list'),
            ],
            [
                types.InlineKeyboardButton(text='реферальная ссылка', callback_data=f'ref'),
            ]]

        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    @staticmethod
    def clear_state():
        key_list = [
            [
                types.InlineKeyboardButton(text='maqrel', callback_data=f'clear_state')
            ]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    @staticmethod
    def ads_list():
        key_list = [[
            types.InlineKeyboardButton(text='✅ Рассылка', callback_data=f'show_list mailing_show'),
            types.InlineKeyboardButton(text='💚 показ', callback_data=f'show_list sharing_show'),
            types.InlineKeyboardButton(text='💹 подписка на канал', callback_data=f'show_list subs_on_channel_ads_show')
        ]]
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    @staticmethod
    def mailing_list():
        key_list = [[
            types.InlineKeyboardButton(text='photos', callback_data=f'mailing_list_photos'),
            types.InlineKeyboardButton(text='video', callback_data=f'mailing_list_video')
        ]]
        return types.InlineKeyboardMarkup(inline_keyboard=key_list)

    @staticmethod
    def show_ads_sharing_list(index, active):
        active = "active" if active is True else "deactivated"
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=f'<-',
                        callback_data=f'show_list_sharing next_or_back {index - 1}'),
                    types.InlineKeyboardButton(
                        text="delete",
                        callback_data=f'show_list_sharing delete {index}'),
                    types.InlineKeyboardButton(
                        text=active,
                        callback_data=f'show_list_sharing active {index} {active}'),
                    types.InlineKeyboardButton(
                        text="->",
                        callback_data=f'show_list_sharing next_or_back {index + 1}')
                ]
            ]
        )