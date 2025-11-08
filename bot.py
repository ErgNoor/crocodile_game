# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import bot, dp # Импортируем bot и dp из config
from handlers import router # Импортируем роутер из handlers

# Включаем логирование
logging.basicConfig(level=logging.INFO)

async def main():
    # Включаем роутер в диспетчер
    dp.include_router(router)

    # Запускаем бота в режиме long polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())