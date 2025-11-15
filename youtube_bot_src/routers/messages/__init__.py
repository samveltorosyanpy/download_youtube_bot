from youtube_bot_src.routers.messages.adminMessages import router as admin_message_router
from youtube_bot_src.routers.messages.userMessages import router as user_message_router
from youtube_bot_src.routers.messages.searchMessages import router as search_message_router
from aiogram import Router



router = Router(name=__name__)

router.include_routers(admin_message_router, user_message_router)
