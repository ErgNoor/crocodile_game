# handlers.py
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from cards import CardManager, CrocodileCard
from config import CARDS_FILE_PATH

# Создаём роутер для обработчиков
router = Router()

# Инициализируем card_manager в этом модуле
card_manager = CardManager(CARDS_FILE_PATH)

logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def send_start(message: Message):
    """Отправляет приветственное сообщение при команде /start."""
    welcome_message = (
        "Привет! 👋\n"
        "Я бот для игры в Крокодила 🦎\n\n"
        "Используй команды ниже, чтобы получить карточку или её часть."
    )
    await message.answer(welcome_message)

@router.message(Command("help"))
async def send_help(message: Message):
    """Отправляет сообщение с описанием команд при команде /help."""
    help_text = (
        "📖 Справка по командам:\n\n"
        "/start - Приветственное сообщение\n"
        "/help - Это сообщение\n"
        "/card - Получить полную карточку (слово, фильм, фраза)\n"
        "/word - Получить только слово/фразу\n"
        "/movie - Получить только название фильма/сериала\n"
        "/phrase - Получить только алогичную фразу\n"
        "/reload_cards - Обновить карточки из файла"
    )
    await message.answer(help_text)

@router.message(Command("card"))
async def send_card(message: Message):
    """Отправляет полную карточку."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return

    message_text = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
    await message.answer(message_text)

@router.message(Command("word"))
async def send_word(message: Message):
    """Отправляет только слово/фразу."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    await message.answer(f"{card.word}")

@router.message(Command("movie"))
async def send_movie(message: Message):
    """Отправляет только фильм/сериал."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    await message.answer(f"{card.movie}")

@router.message(Command("phrase"))
async def send_phrase(message: Message):
    """Отправляет только алогичную фразу."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    await message.answer(f"{card.phrase}")

@router.message(Command("reload_cards"))
async def send_reload_cards(message: Message):
    """Обработчик команды /reload_cards."""
    logger.info(f"Получена команда /reload_cards от {message.from_user.id}")
    card_manager._load_cards()
    await message.answer("Карточки обновлены из файла.")
