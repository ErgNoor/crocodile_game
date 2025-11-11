# handlers.py
import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from cards import CardManager
from config import WORDS_FILE_PATH, MOVIES_FILE_PATH, PHRASES_FILE_PATH
from text_loader import load_text_from_file
from pathlib import Path

# Создаём роутер для обработчиков
router = Router()

# Инициализируем card_manager в этом модуле с новыми путями
card_manager = CardManager(WORDS_FILE_PATH, MOVIES_FILE_PATH, PHRASES_FILE_PATH)

logger = logging.getLogger(__name__)

# --- Пути к файлам с текстами ---
WELCOME_MESSAGE_PATH = Path("resources/welcome_message.txt")
HELP_MESSAGE_PATH = Path("resources/help_message.txt")

# --- Создание клавиатуры (с русскими кнопками, без /reload_cards) ---
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Карточка"), KeyboardButton(text="Слово")],
            [KeyboardButton(text="Фильм/мультфильм(сериал)"), KeyboardButton(text="Фраза")],
            [KeyboardButton(text="Помощь")], # Убрана кнопка /reload_cards
        ],
        resize_keyboard=True,
        one_time_keyboard=False # Клавиатура не исчезает после нажатия
    )
    return keyboard

@router.message(Command("start"))
async def send_start(message: Message):
    """Отправляет приветственное сообщение при команде /start."""
    welcome_message = load_text_from_file(WELCOME_MESSAGE_PATH)
    keyboard = get_main_keyboard()
    await message.answer(welcome_message, reply_markup=keyboard)

@router.message(Command("help"))
async def send_help(message: Message):
    """Отправляет сообщение с описанием команд при команде /help."""
    help_text = load_text_from_file(HELP_MESSAGE_PATH)
    keyboard = get_main_keyboard()
    await message.answer(help_text, reply_markup=keyboard)

@router.message(Command("card"))
async def send_card(message: Message):
    """Отправляет полную карточку."""
    card_parts = card_manager.get_random_card_parts()
    if not card_parts:
        await message.answer("Карточки не загружены или файлы пусты.")
    else:
        word, movie, phrase = card_parts
        message_text = f"1) {word}\n2) {movie}\n3) {phrase}"
        keyboard = get_main_keyboard()
        await message.answer(message_text, reply_markup=keyboard)

@router.message(Command("word"))
async def send_word(message: Message):
    """Отправляет только слово/фразу."""
    card_parts = card_manager.get_random_card_parts()
    if not card_parts:
        await message.answer("Карточки не загружены или файлы пусты.")
    else:
        word, _, _ = card_parts
        keyboard = get_main_keyboard()
        await message.answer(f"{word}", reply_markup=keyboard)

@router.message(Command("movie"))
async def send_movie(message: Message):
    """Отправляет только фильм/сериал."""
    card_parts = card_manager.get_random_card_parts()
    if not card_parts:
        await message.answer("Карточки не загружены или файлы пусты.")
    else:
        _, movie, _ = card_parts
        keyboard = get_main_keyboard()
        await message.answer(f"{movie}", reply_markup=keyboard)

@router.message(Command("phrase"))
async def send_phrase(message: Message):
    """Отправляет только алогичную фразу."""
    card_parts = card_manager.get_random_card_parts()
    if not card_parts:
        await message.answer("Карточки не загружены или файлы пусты.")
    else:
        _, _, phrase = card_parts
        keyboard = get_main_keyboard()
        await message.answer(f"{phrase}", reply_markup=keyboard)

@router.message(Command("reload_cards"))
async def send_reload_cards(message: Message):
    """Обработчик команды /reload_cards."""
    card_manager.reload_data()
    # Отправляем сообщение без клавиатуры, чтобы не добавлять кнопку снова
    await message.answer("Карточки обновлены из файлов.")

# --- Обработчик нажатия кнопок (с русскими текстами, без /reload_cards) ---
# F.text.in_ проверяет, совпадает ли текст сообщения с одним из указанных
@router.message(F.text.in_([
    'Карточка',
    'Слово',
    'Фильм/мультфильм(сериал)',
    'Фраза',
    'Помощь',
]))
async def handle_button_click(message: Message):
    """
    Обрабатывает нажатие кнопок, которые отправляют команды.
    """
    user_text = message.text
    # Используем match/case для сопоставления текста кнопки
    match user_text:
        case 'Карточка':
            card_parts = card_manager.get_random_card_parts()
            if not card_parts:
                await message.answer("Карточки не загружены или файлы пусты.")
            else:
                word, movie, phrase = card_parts
                message_text = f"1) {word}\n2) {movie}\n3) {phrase}"
                keyboard = get_main_keyboard()
                await message.answer(message_text, reply_markup=keyboard)
        case 'Слово':
            card_parts = card_manager.get_random_card_parts()
            if not card_parts:
                await message.answer("Карточки не загружены или файлы пусты.")
            else:
                word, _, _ = card_parts
                keyboard = get_main_keyboard()
                await message.answer(f"{word}", reply_markup=keyboard)
        case 'Фильм/мультфильм(сериал)':
            card_parts = card_manager.get_random_card_parts()
            if not card_parts:
                await message.answer("Карточки не загружены или файлы пусты.")
            else:
                _, movie, _ = card_parts
                keyboard = get_main_keyboard()
                await message.answer(f"{movie}", reply_markup=keyboard)
        case 'Фраза':
            card_parts = card_manager.get_random_card_parts()
            if not card_parts:
                await message.answer("Карточки не загружены или файлы пусты.")
            else:
                _, _, phrase = card_parts
                keyboard = get_main_keyboard()
                await message.answer(f"{phrase}", reply_markup=keyboard)
        case 'Помощь':
            help_text = load_text_from_file(HELP_MESSAGE_PATH)
            keyboard = get_main_keyboard()
            await message.answer(help_text, reply_markup=keyboard)
        # else: можно добавить case _ для обработки неизвестных кнопок, если нужно
        # case _:
        #     logger.warning(f"Получен неизвестный текст от кнопки: '{user_text}'")
        #     await message.answer("Неизвестная команда.")
