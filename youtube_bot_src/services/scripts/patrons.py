from aiogram import types
from youtube_bot_src.services.db import Users_class, Sharing_class
from consts import *
from youtube_bot_src.services.scripts.utils import send_ads

async def CheckAdsForDownload(user_id: int):
    user_data = Users_class.get(user_id=user_id)
    ads_list = Sharing_class.get_all_active()

    if user_data.last_activity % SHOW_COUNT == 0 and user_data.last_activity != 0 and len(ads_list) != 0:
        if user_data.last_activity // 5 - 1 > len(ads_list) - 1:
            user_data.last_activity = 5

        await send_ads(user_id, ads_list[int(user_data.last_activity // 5 - 1)])

    Users_class.update_by_id(user_id=user_id, last_activity=user_data.last_activity+1)



