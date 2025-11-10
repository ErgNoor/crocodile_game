# cards.py
import json
import logging
from pathlib import Path
from random import choice

logger = logging.getLogger(__name__)

class CardManager:
    def __init__(self, words_file_path: Path, movies_file_path: Path, phrases_file_path: Path):
        self.words_file_path = words_file_path
        self.movies_file_path = movies_file_path
        self.phrases_file_path = phrases_file_path

        # Списки для хранения данных
        self.words: list[str] = []
        self.movies: list[str] = []
        self.phrases: list[str] = []

        # Загружаем данные из файлов
        self._load_words()
        self._load_movies()
        self._load_phrases()

    def _load_words(self):
        """Загружает слова/фразы из JSON-файла."""
        try:
            with self.words_file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                self.words = data
                logger.info(f"Загружено {len(self.words)} слов/фраз из {self.words_file_path}")
            else:
                logger.error(f"Файл {self.words_file_path} не содержит список.")
                self.words = []
        except FileNotFoundError:
            logger.error(f"Файл {self.words_file_path} не найден.")
            self.words = []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка чтения JSON из {self.words_file_path}: {e}")
            self.words = []

    def _load_movies(self):
        """Загружает фильмы/сериалы из JSON-файла."""
        try:
            with self.movies_file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                self.movies = data
                logger.info(f"Загружено {len(self.movies)} фильмов/сериалов из {self.movies_file_path}")
            else:
                logger.error(f"Файл {self.movies_file_path} не содержит список.")
                self.movies = []
        except FileNotFoundError:
            logger.error(f"Файл {self.movies_file_path} не найден.")
            self.movies = []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка чтения JSON из {self.movies_file_path}: {e}")
            self.movies = []

    def _load_phrases(self):
        """Загружает алогичные фразы из JSON-файла."""
        try:
            with self.phrases_file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                self.phrases = data
                logger.info(f"Загружено {len(self.phrases)} алогичных фраз из {self.phrases_file_path}")
            else:
                logger.error(f"Файл {self.phrases_file_path} не содержит список.")
                self.phrases = []
        except FileNotFoundError:
            logger.error(f"Файл {self.phrases_file_path} не найден.")
            self.phrases = []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка чтения JSON из {self.phrases_file_path}: {e}")
            self.phrases = []

    def reload_data(self):
        """Перезагружает все списки из файлов."""
        logger.info("Перезагрузка данных из файлов...")
        self._load_words()
        self._load_movies()
        self._load_phrases()
        logger.info("Перезагрузка данных завершена.")

    def get_random_card_parts(self) -> tuple[str, str, str] | None:
        """
        Возвращает кортеж (word, movie, phrase) случайной карточки или None,
        если один из списков пуст.
        """
        if not self.words or not self.movies or not self.phrases:
            logger.warning("Один или несколько списков пусты. Невозможно создать карточку.")
            return None

        word = choice(self.words)
        movie = choice(self.movies)
        phrase = choice(self.phrases)
        return word, movie, phrase
