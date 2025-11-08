# cards.py
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from random import choice

logger = logging.getLogger(__name__)

@dataclass
class CrocodileCard:
    word: str
    movie: str
    phrase: str

class CardManager:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.cards: list[CrocodileCard] = []
        self._load_cards()

    def _load_cards(self):
        """Загружает карточки из JSON-файла."""
        try:
            with self.file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            self.cards = [CrocodileCard(**item) for item in data]
            logger.info(f"Загружено {len(self.cards)} карточек из {self.file_path}")
        except FileNotFoundError:
            logger.error(f"Файл {self.file_path} не найден.")
            self.cards = []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка чтения JSON из {self.file_path}: {e}")
            self.cards = []
        except TypeError as e:
            logger.error(f"Ошибка структуры данных в {self.file_path}: {e}")
            self.cards = []

    def get_random_card(self) -> CrocodileCard | None:
        """Возвращает случайную карточку или None, если карточки отсутствуют."""
        if not self.cards:
            return None
        return choice(self.cards)

    # Дополнительный метод, если нужен доступ ко всем частям за раз
    # def get_random_card_parts(self) -> tuple[str, str, str] | None:
    #     """Возвращает кортеж (word, movie, phrase) случайной карточки или None."""
    #     card = self.get_random_card()
    #     if card:
    #         return card.word, card.movie, card.phrase
    #     return None
