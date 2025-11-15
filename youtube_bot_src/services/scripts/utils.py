from consts import *
import json
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from youtube_bot_src.keyboards import user_keyboards


async def send_ads(user_id, ads):
    butt_replace = json.loads(ads.buttons.replace('\'', '"'))
    button = None if ads.buttons is None else user_keyboards.create_keyboard_ads(butt_replace)
    try:
        medias = json.loads(ads.media.replace('\'', '"'))
        if 'photo' in medias.keys():
            await bot.send_photo(
                chat_id=user_id,
                photo=medias['photo'],
                caption=ads.text,
                reply_markup=button,
                parse_mode=ParseMode.HTML
            )
        elif 'video' in medias.keys():
            await bot.send_video(
                chat_id=user_id,
                video=medias['video'],
                caption=ads.text,
                reply_markup=button,
                parse_mode=ParseMode.HTML
            )
    except json.decoder.JSONDecodeError:
        if ads.text:
            await bot.send_message(
                chat_id=user_id,
                text=ads.text,
                reply_markup=button,
                parse_mode=ParseMode.HTML
            )
    except Exception:
        return 1


async def send_ads_for_admin(admin_id, ads, buttons=None):
    try:
        medias = json.loads(ads.media.replace('\'', '"'))
        if 'photo' in medias.keys():
            await bot.send_photo(
                chat_id=admin_id,
                photo=medias['photo'],
                caption=ads.text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML
            )
        elif 'video' in medias.keys():
            await bot.send_video(
                chat_id=admin_id,
                video=medias['video'],
                caption=ads.text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML
            )
    except json.decoder.JSONDecodeError:
        if ads.text:
            await bot.send_message(
                chat_id=admin_id,
                text=ads.text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML
            )
    except Exception:
        pass



