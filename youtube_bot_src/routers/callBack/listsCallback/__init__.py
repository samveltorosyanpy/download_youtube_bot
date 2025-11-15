from aiogram import Router
from youtube_bot_src.routers.callBack.listsCallback.ads_sharing import router as ads_sharing_routers

ads_routers = Router(name=__name__)

ads_routers.include_routers(ads_sharing_routers)