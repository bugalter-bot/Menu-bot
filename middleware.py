from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config import ADMIN_ID


class AdminOnlyMiddleware(BaseMiddleware):
    """Bu shaxsiy bot bo'lgani uchun faqat ADMIN_ID ga tegishli foydalanuvchiga javob beradi."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user and ADMIN_ID and user.id != ADMIN_ID:
            return
        return await handler(event, data)
