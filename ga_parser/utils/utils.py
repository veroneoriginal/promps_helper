"""
Вспомогательные функции
"""

import re
from html import unescape
from pathlib import Path
import random

from ga_parser.parser.requests_funcs import get_image


def clean_text(raw_text: str) -> str:
    """
    Очищает строку от HTML-тегов, символов переноса строки, декодирует HTML-символы.
    убирает множественные пробелы.

    :param raw_text: Строка с HTML-тегами
    :return: Очищенная строка
    """

    if not isinstance(raw_text, str):
        return raw_text  # Возвращаем значение как есть, если это не строка
    # Убираем HTML-теги
    no_html = re.sub(r'<[^>]*>', ' ', raw_text)
    # Убираем символы переноса строки и лишние пробелы
    no_newlines = re.sub(r'\s+', ' ', no_html).strip()
    # Раскодируем HTML-символы
    clean = unescape(no_newlines)
    # Заменяем множественные пробелы на один
    return re.sub(r'\s{2,}', ' ', clean)


def clean_value_str_in_dict(source_dict: dict) -> dict:
    """
    Формирует новый словарь с очищенными значениями от тегов,
    лишних пробелов и т.д.

    :param source_dict: исходный словарь
    :return: итоговый "чистый" словарь

    """

    return {key: clean_text(value) for key, value in source_dict.items()}


def list_to_dict(data: list) -> dict:
    """
    Конвертирует список вида:
    "attributes": [
                {
                    "key": "тип продукта",
                    "value": "шампунь"
                },
                {
                    "key": "для кого",
                    "value": "женский"
                },
            ]
    в словарь вида:
    {
        "тип продукта": "шампунь",
        "для кого": "женский",
    }
    """

    return {item["key"]: item["value"] for item in data}


def create_full_link_to_image(link: str) -> str:
    """
    Формирует полную ссылку к изображению продукта в формате .jpg

    :param link: ссылка на изображение без вставленных параметров
    :return: готовая ссылка
    """

    link = link.replace('${screen}', 'fullhd')
    return link.replace('${format}', 'jpg')


def calculate_price_ml(
        units: str,
        price: int | float,
        ml: int = 100
) -> int | float:
    """
    Функция рассчитывает стоимость за определённое количество мл.

    :param units: количество мл в товаре
    :param price: стоимость товара
    :param ml: на какое количество мл рассчитываем стоимость

    :return: стоимость за ml
    """
    units = int(units)

    if units <= 0:
        raise ValueError("Количество мл должно быть больше 0")
    return int((price / units) * ml)


def download_image(
        url: str,
        product_title: str,
        image_dir_path: Path,
):
    """
    Сохраняет изображение средства в папку

    :param url: ссылка на изображение средства
    :param product_title: название средства
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :return:
    """

    response = get_image(url)
    # Удаляем все символы, кроме букв и цифр, заменяем их на "_"
    sanitized_title = re.sub(
        pattern=r"[^a-zA-Z0-9]+",
        repl="_",
        string=product_title.strip().lower()
    )
    save_path = image_dir_path / f"{sanitized_title}.jpg"

    # Открываем файл в бинарном режиме для записи
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
        print(f"Изображение успешно сохранено в {save_path}")


def path_to_universal(path: str) -> Path:
    """
    Приводит путь к платформо-независимому (Windows, Linux, MacOS...)

    :param path: исходный путь
    :return: платформо-независимый путь
    """

    return Path(path).resolve()


def check_or_create_dir(dir_path: str) -> None:
    """
    Создаёт папку по указанному пути, если её нет

    :param dir_path: путь к папке
    """

    image_dir_path = path_to_universal(dir_path)

    # Проверяем существование папки, если нет - создаём
    if not image_dir_path.exists():
        print(f'Папка {image_dir_path} не найдена. Создаём...')
        image_dir_path.mkdir(parents=True, exist_ok=True)


def random_between(num: int, lag: int = 5) -> int:
    """
    Возвращает случайное число между исходным и добавленным к исходному

    :param num: исходное число
    :param lag: число, которое добавим к исходному
    :return: случайное число из полученного диапазона
    """
    return random.randint(num, num + lag)
