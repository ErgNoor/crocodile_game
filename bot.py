import json
import logging
from random import choice
from dataclasses import dataclass
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем dataclass для карточки
@dataclass
class CrocodileCard:
    word: str
    movie: str
    phrase: str

# Путь к файлу с карточками
CARDS_FILE_PATH = Path("cards.json")

def load_cards_from_json(file_path: Path) -> list[CrocodileCard]:
    """Загружает карточки из JSON-файла."""
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        # Преобразуем словари из JSON в экземпляры dataclass
        cards = [CrocodileCard(**item) for item in data]
        logger.info(f"Загружено {len(cards)} карточек из {file_path}")
        return cards
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка чтения JSON из {file_path}: {e}")
        return []
    except TypeError as e:
        logger.error(f"Ошибка структуры данных в {file_path}: {e}")
        return []

# Загружаем карточки при запуске скрипта
CARDS = load_cards_from_json(CARDS_FILE_PATH)

async def send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет полную карточку."""
    if not CARDS:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return

    card = choice(CARDS)
    message = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
    await update.message.reply_text(message)

async def send_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только слово/фразу."""
    if not CARDS:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return

    card = choice(CARDS)
    await update.message.reply_text(f"{card.word}")

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только фильм/сериал."""
    if not CARDS:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return

    card = choice(CARDS)
    await update.message.reply_text(f"{card.movie}")

async def send_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только алогичную фразу."""
    if not CARDS:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return

    card = choice(CARDS)
    await update.message.reply_text(f"{card.phrase}")

def main() -> None:
    """Запуск бота."""
    # Замените 'YOUR_TOKEN' на токен, который вы получили от @BotFather
    application = Application.builder().token("YOUR_TOKEN").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("card", send_card))
    application.add_handler(CommandHandler("word", send_word))
    application.add_handler(CommandHandler("movie", send_movie))
    application.add_handler(CommandHandler("phrase", send_phrase))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()