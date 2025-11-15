from youtube_bot_src.routers.messages import router as message_routers, search_message_router
from youtube_bot_src.routers.commands import router as commands_routers
from youtube_bot_src.routers.callBack import router as callback_routers
from youtube_bot_src.filters.MyFilters import MainFilter
from aiogram import Router

router = Router(name=__name__)
router.message.filter(MainFilter())
router.include_routers(message_routers, commands_routers, callback_routers, search_message_router)
