from aiogram import Router
from youtube_bot_src.routers.callBack.youtubeCallBack import router as youtube_callback_router
from youtube_bot_src.routers.callBack.Mp3EffectsCallBack import router as mp3_edited_router
from youtube_bot_src.routers.callBack.AdminCallBack import router as admin_router
from youtube_bot_src.routers.callBack.UserCallBack import router as user_router
from youtube_bot_src.routers.callBack.TikTokCallBack import router as tiktok_router

router = Router(name=__name__)
router.include_routers(tiktok_router, youtube_callback_router, mp3_edited_router, admin_router, user_router)