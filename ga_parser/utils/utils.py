"""
Вспомогательные функции
"""
import re
from functools import wraps
from html import unescape
from pathlib import Path
import random

import requests
from requests.exceptions import (
    RequestException,
    ReadTimeout,
)

from PIL import Image, ImageDraw, ImageFont

from ga_parser.utils.requests_funcs import get_image






def clean_text_2(raw_text: str) -> str:
    """
    Очищает строку от HTML-тегов, символов переноса строки, декодирует HTML-символы.
    убирает множественные пробелы.

    :param raw_text: Строка с HTML-тегами
    :return: Очищенная строка
    """

    if not isinstance(raw_text, str):
        return raw_text  # Возвращаем значение как есть, если это не строка

    # Убираем множественные пробелы, заменяя их на один
    cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()

    return cleaned_text


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
) -> int | float | None:
    """
    Функция рассчитывает стоимость за определённое количество мл.

    :param units: количество мл в товаре
    :param price: стоимость товара
    :param ml: на какое количество мл рассчитываем стоимость

    :return: стоимость за ml
    """
    if not units or not units.isdigit():
        return None

    units = int(units)

    if units <= 0:
        raise ValueError("Количество мл должно быть больше 0")
    return int((price / units) * ml)


def clean_product_name(
        product_title: str,
) -> str:
    """
    Удаляем все символы, кроме букв и цифр, заменяем их на "_"

    :param product_title: "Грязное" название средства
    :return: отчищенное имя
    """

    return re.sub(
        pattern=r"[^a-zA-Z0-9]+",
        repl="_",
        string=product_title.strip().lower()
    )


def download_image(
        url: str,
        file_save_path: str,
) -> None:
    """
    Сохраняет изображение средства в папку

    :param url: ссылка на изображение средства
    :param file_save_path: путь для сохранения файла
    :return: None
    """

    response = get_image(url)

    # Открываем файл в бинарном режиме для записи
    with open(file_save_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)


def add_text_to_image(
        open_full_path: str,
        text: str,
        save_full_path: str | None = None,
        x_y_offset: tuple = (20, 40),
) -> None:
    """
    Добавляет текст "Источник" на изображение

    :param open_full_path: полное имя файла (путь) для открытия
    :param save_full_path: полное имя файла (путь) для сохранения
    :param text: текст для добавления
    :param x_y_offset: отступы по осям
    :return: None
    """
    FONT_NAME = "Roboto-Regular.ttf"
    FONT_SIZE = 20
    FONT_COLOR = (0, 0, 0, 100)

    image = Image.open(fp=open_full_path).convert("RGBA")
    font = load_font(font_name=FONT_NAME, font_size=FONT_SIZE)
    text_layer = Image.new(mode="RGBA", size=image.size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    coordinate = (x_y_offset[0], image.size[1] - x_y_offset[1])
    text_to_paste = f'Источник: {text}'
    draw.text(xy=coordinate, text=text_to_paste, fill=FONT_COLOR, font=font)
    combined = Image.alpha_composite(image, text_layer).convert("RGB")
    save_path = save_full_path if save_full_path else open_full_path
    combined.save(fp=save_path)


def load_font(
        font_name: str = "Roboto-Regular.ttf",
        font_size: int = 40) -> ImageFont:
    """
    Загружает шрифт для PIL

    :param font_name: имя шрифта
    :param font_size: размер шрифта
    :return: None
    """

    font_path = Path.cwd() / '00_base/source/fonts' / font_name
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        print(
            ('Для нанесения источника на изображение '
             'не удалось загрузить шрифт, использую стандартный шрифт')
        )
        return ImageFont.load_default()


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


def handle_index_error():
    """
    Декоратор для обработки IndexError и возврата заданного значения.

    :param default_value: Значение, которое будет возвращено при ошибке IndexError.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IndexError:
                return None

        return wrapper

    return decorator


def is_vpn_enabled() -> bool:
    """
    Проверяет, включен ли VPN
    """

    try:
        response = requests.get("https://goldapple.ru/19000324846-keratin-works", timeout=10)
        status = response.status_code

        # Проверяем, не является ли IP локальным
        if status == 403:
            return True
        return False

    except (
            RequestException,
            ReadTimeout
    ):
        print("🚫 Нет соединения, возможно VPN включен!")
        return False
