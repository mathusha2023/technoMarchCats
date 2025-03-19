from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import BANNED_USERS


class BannedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in BANNED_USERS
