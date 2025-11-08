# config.py
import os
from pathlib import Path
from dotenv import load_dotenv # Импортируем функцию

# Загружаем переменные из .env файла (если он существует)
# load_dotenv() ищет файл .env в текущей директории по умолчанию
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set.")

CARDS_FILE_PATH = Path(os.getenv("CARDS_FILE_PATH", "cards.json"))