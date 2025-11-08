# bot.py
import logging
from config import BOT_TOKEN, CARDS_FILE_PATH
from cards import CardManager
# Убираем импорт card_manager из handlers
from handlers import send_card, send_word, send_movie, send_phrase, send_start, send_help

# Инициализируем card_manager ТОЛЬКО в bot.py
card_manager = CardManager(CARDS_FILE_PATH)

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from telegram.ext import Application, CommandHandler, ContextTypes

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Помещаем card_manager в bot_data, чтобы он был доступен в обработчиках
    application.bot_data['card_manager'] = card_manager

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", send_start))
    application.add_handler(CommandHandler("help", send_help))
    application.add_handler(CommandHandler("card", send_card))
    application.add_handler(CommandHandler("word", send_word))
    application.add_handler(CommandHandler("movie", send_movie))
    application.add_handler(CommandHandler("phrase", send_phrase))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()