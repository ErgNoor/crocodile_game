# middlewares.py
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для логирования действий пользователей.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем информацию о пользователе
        user_id = event.from_user.id
        username = event.from_user.username or "N/A"
        full_name = event.from_user.full_name # Используем full_name вместо username для большей информации

        # Определяем тип действия (команда или текст)
        action = "unknown"
        action_detail = "unknown"

        if event.text:
            text = event.text
            if text.startswith('/'):
                action = "command"
                action_detail = text.split()[0] # Берём только команду, например, /card
            else:
                action = "button_click" # Считаем, что любой текст не-команда - это нажатие кнопки
                action_detail = text

        # Логируем событие
        logger.info(f"Пользователь {full_name} (ID: {user_id}, Username: {username}) отправил {action}: {action_detail}")

        # Вызываем следующий обработчик
        result = await handler(event, data)
        return result
