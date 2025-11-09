# handlers.py
import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from cards import CardManager, CrocodileCard
from config import CARDS_FILE_PATH

# Создаём роутер для обработчиков
router = Router()

# Инициализируем card_manager в этом модуле
card_manager = CardManager(CARDS_FILE_PATH)

logger = logging.getLogger(__name__)

# --- Создание клавиатуры ---
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Карточка"), KeyboardButton(text="Слово")],
            [KeyboardButton(text="Фильм/мультфильм(сериал)"), KeyboardButton(text="Фраза")],
            [KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False # Клавиатура не исчезает после нажатия
    )
    return keyboard

@router.message(Command("start"))
async def send_start(message: Message):
    """Отправляет приветственное сообщение при команде /start."""
    welcome_message = (
        "Привет! 👋\n"
        "Я бот для игры в Крокодила 🦎\n\n"
        "Используй команды или кнопки ниже, чтобы получить карточку или её часть."
        "Карточки построены по принципу: "
        "1) Слово или фраза (1 или 2 слова)"
        "2) Название фильма/мультфильма/сериала/мультсериала"
        "3) Небольшая алогичная фраза из не связанных между собой слов (максимум - 6 слов)"
    )
    keyboard = get_main_keyboard()
    await message.answer(welcome_message, reply_markup=keyboard)

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
    keyboard = get_main_keyboard()
    await message.answer(help_text, reply_markup=keyboard)

@router.message(Command("card"))
async def send_card(message: Message):
    """Отправляет полную карточку."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return

    message_text = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
    keyboard = get_main_keyboard()
    await message.answer(message_text, reply_markup=keyboard)

@router.message(Command("word"))
async def send_word(message: Message):
    """Отправляет только слово/фразу."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    keyboard = get_main_keyboard()
    await message.answer(f"{card.word}", reply_markup=keyboard)

@router.message(Command("movie"))
async def send_movie(message: Message):
    """Отправляет только фильм/сериал."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    keyboard = get_main_keyboard()
    await message.answer(f"{card.movie}", reply_markup=keyboard)

@router.message(Command("phrase"))
async def send_phrase(message: Message):
    """Отправляет только алогичную фразу."""
    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await message.answer("Карточки не загружены или файл пуст.")
        return
    keyboard = get_main_keyboard()
    await message.answer(f"{card.phrase}", reply_markup=keyboard)

@router.message(Command("reload_cards"))
async def send_reload_cards(message: Message):
    """Обработчик команды /reload_cards."""
    logger.info(f"Получена команда /reload_cards от {message.from_user.id}")
    card_manager._load_cards()
    keyboard = get_main_keyboard()
    await message.answer("Карточки обновлены из файла.", reply_markup=keyboard)

# --- НОВОЕ: Обработчик нажатия кнопок ---
# F.text.in_ проверяет, совпадает ли текст сообщения с одним из указанных
@router.message(F.text.in_(['/card', '/word', '/movie', '/phrase', '/help', '/reload_cards']))
async def handle_button_click(message: Message):
    """
    Обрабатывает нажатие кнопок, которые отправляют команды.
    """
    # Так как кнопки отправляют команды, мы можем просто вызвать соответствующую логику
    # или переадресовать к основному обработчику команд.
    # В aiogram удобно использовать подстановку сообщения.
    # Однако, для простоты, мы можем вызвать нужную функцию напрямую.

    user_text = message.text
    logger.info(f"Получено текстовое сообщение от кнопки: '{user_text}' от {message.from_user.id}")

    if user_text == '/card':
        card: CrocodileCard | None = card_manager.get_random_card()
        if not card:
            await message.answer("Карточки не загружены или файл пуст.")
            return
        message_text = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
        keyboard = get_main_keyboard()
        await message.answer(message_text, reply_markup=keyboard)
    elif user_text == '/word':
        card: CrocodileCard | None = card_manager.get_random_card()
        if not card:
            await message.answer("Карточки не загружены или файл пуст.")
            return
        keyboard = get_main_keyboard()
        await message.answer(f"{card.word}", reply_markup=keyboard)
    elif user_text == '/movie':
        card: CrocodileCard | None = card_manager.get_random_card()
        if not card:
            await message.answer("Карточки не загружены или файл пуст.")
            return
        keyboard = get_main_keyboard()
        await message.answer(f"{card.movie}", reply_markup=keyboard)
    elif user_text == '/phrase':
        card: CrocodileCard | None = card_manager.get_random_card()
        if not card:
            await message.answer("Карточки не загружены или файл пуст.")
            return
        keyboard = get_main_keyboard()
        await message.answer(f"{card.phrase}", reply_markup=keyboard)
    elif user_text == '/help':
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
        keyboard = get_main_keyboard()
        await message.answer(help_text, reply_markup=keyboard)
    elif user_text == '/reload_cards':
        logger.info(f"Получена команда /reload_cards от {message.from_user.id}")
        card_manager._load_cards()
        keyboard = get_main_keyboard()
        await message.answer("Карточки обновлены из файла.", reply_markup=keyboard)
