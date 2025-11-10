# config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set.")

# Пути к файлам с данными
WORDS_FILE_PATH = Path(os.getenv("WORDS_FILE_PATH", "words.json"))
MOVIES_FILE_PATH = Path(os.getenv("MOVIES_FILE_PATH", "movies.json"))
PHRASES_FILE_PATH = Path(os.getenv("PHRASES_FILE_PATH", "phrases.json"))

# Создаём экземпляр Bot с DefaultBotProperties
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаём экземпляр Dispatcher
dp = Dispatcher()