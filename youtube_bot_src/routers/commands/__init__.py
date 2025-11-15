__all__ = ('router',)

from aiogram import Router
from youtube_bot_src.routers.commands.adminCommands import router as admin_commands_router
from youtube_bot_src.routers.commands.userCommands import router as user_commands_router


router = Router(name=__name__)


router.include_routers(admin_commands_router, user_commands_router)