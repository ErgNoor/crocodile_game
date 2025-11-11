# text_loader.py
from pathlib import Path

def load_text_from_file(file_path: Path) -> str:
    """
    Читает текст из файла и возвращает его содержимое.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return "Текст не найден."
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {e}")
        return "Текст не найден."
