# handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from cards import CardManager, CrocodileCard # Импортируем только классы

# Убираем глобальную переменную card_manager: CardManager

async def send_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    welcome_message = (
        "Привет! 👋\n"
        "Я бот для игры в Крокодила 🦎\n\n"
        "Используй команды ниже, чтобы получить карточку или её часть."
    )
    await update.message.reply_text(welcome_message)

async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с описанием команд при команде /help."""
    help_text = (
        "📖 Справка по командам:\n\n"
        "/start - Приветственное сообщение\n"
        "/help - Это сообщение\n"
        "/card - Получить полную карточку (слово, фильм, фраза)\n"
        "/word - Получить только слово/фразу\n"
        "/movie - Получить только название фильма/сериала\n"
        "/phrase - Получить только алогичную фразу"
    )
    await update.message.reply_text(help_text)

async def send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет полную карточку."""
    # Получаем card_manager из bot_data
    card_manager: CardManager = context.application.bot_data.get('card_manager')
    if not card_manager:
        # Это может произойти, если bot_data не был инициализирован
        logger.error("card_manager не найден в bot_data!")
        await update.message.reply_text("Ошибка: внутренняя ошибка бота.")
        return

    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return

    message = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
    await update.message.reply_text(message)

async def send_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только слово/фразу."""
    # Получаем card_manager из bot_data
    card_manager: CardManager = context.application.bot_data.get('card_manager')
    if not card_manager:
        logger.error("card_manager не найден в bot_data!")
        await update.message.reply_text("Ошибка: внутренняя ошибка бота.")
        return

    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return
    await update.message.reply_text(f"{card.word}")

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только фильм/сериал."""
    # Получаем card_manager из bot_data
    card_manager: CardManager = context.application.bot_data.get('card_manager')
    if not card_manager:
        logger.error("card_manager не найден в bot_data!")
        await update.message.reply_text("Ошибка: внутренняя ошибка бота.")
        return

    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return
    await update.message.reply_text(f"{card.movie}")

async def send_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только алогичную фразу."""
    # Получаем card_manager из bot_data
    card_manager: CardManager = context.application.bot_data.get('card_manager')
    if not card_manager:
        logger.error("card_manager не найден в bot_data!")
        await update.message.reply_text("Ошибка: внутренняя ошибка бота.")
        return

    card: CrocodileCard | None = card_manager.get_random_card()
    if not card:
        await update.message.reply_text("Карточки не загружены или файл пуст.")
        return
    await update.message.reply_text(f"{card.phrase}")