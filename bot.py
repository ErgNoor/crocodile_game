import logging
from random import choice
from dataclasses import dataclass
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

# Встроенный список карточек
# Можно легко заменить на чтение из JSON файла в будущем
CARDS = [
    CrocodileCard(word="Снегопад", movie="Терминатор", phrase="Белка под водой"),
    CrocodileCard(word="Чистый пол", movie="Штрафной удар", phrase="Волынка пьёт виски со льдом"),
    # Добавьте сюда больше карточек по образцу
    CrocodileCard(word="Кот в сапогах", movie="Матрица", phrase="Собака играет на флейте"),
    CrocodileCard(word="Горячий лёд", movie="Игра престолов", phrase="Лампочка боится темноты"),
    CrocodileCard(word="Звонкий нос", movie="Аватар", phrase="Карандаш рисует в облаках"),
    CrocodileCard(word="Сломанная радуга", movie="Форсаж", phrase="Чайник спит под столом"),
    CrocodileCard(word="Танцующий чайник", movie="Скуби-Ду", phrase="Книга читает ученика"),
    CrocodileCard(word="Прыгающий шкаф", movie="Холодное сердце", phrase="Микроволновка греет мороз"),
    CrocodileCard(word="Плывущий вертолёт", movie="Рик и Морти", phrase="Носки вяжут свитер"),
    CrocodileCard(word="Плачущий смех", movie="Смешарики", phrase="Тучка танцует под дождиком"),
    # ... и так далее
]

async def send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет полную карточку."""
    card = choice(CARDS)
    message = f"1) {card.word}\n2) {card.movie}\n3) {card.phrase}"
    await update.message.reply_text(message)

async def send_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только слово/фразу."""
    card = choice(CARDS)
    await update.message.reply_text(f"{card.word}")

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только фильм/сериал."""
    card = choice(CARDS)
    await update.message.reply_text(f"{card.movie}")

async def send_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет только алогичную фразу."""
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
