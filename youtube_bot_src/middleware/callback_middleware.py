from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from consts import logger_bot


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0
        # self.s = s

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        logger_bot.info(self.counter)
        data['counter'] = self.counter
        return await handler(event, data)
