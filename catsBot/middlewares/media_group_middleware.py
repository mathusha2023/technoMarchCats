import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


# мидльварь для вытягивания всех объектов медиа группы
class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = 0.6):
        self.delay = delay  # задержка после которой прием медиа будет окончен

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return  # Не пропускаем событие дальше
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)