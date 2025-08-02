""" Логика парсера """

import json
import re

from ga_parser.parser_v1.parser.generation_product_data import get_product_data_dict
from ga_parser.utils.requests_funcs import get_page
from ga_parser.utils.utils import download_image


def get_product_card(html_text: str) -> dict | None:
    """
    Забирает блок с информацией о средстве,
    преобразует строку JSON в словарь Python.

    :param html_text: строка с html-содержимым страницы
    :return: str
    """

    match = re.search(
        r"window\.serverCache\['productCard']\s*=\s*({.*?});",
        html_text,
        re.DOTALL
    )

    if match:
        product_card_data = match.group(1)  # Выделяем содержимое объекта
        try:
            print("Получили карточку средства")
            return json.loads(product_card_data)['data']
        except json.JSONDecodeError as e:
            print("Ошибка при получении карточки средства:", e)
            return None
    else:
        print("Карточка средства не найдена")
        return None


def get_product_dict(url: str) -> dict | None:
    """
    Получает карточку продукта в виде словаря

    :param url: url средства на сайте Золотого Яблока
    :return: dict
    """

    html = get_page(url)
    return get_product_card(html)


def parse_product(
        url: str,
        image_dir_path: str,
) -> dict | None:
    """
    Управляющая функция.
    Парсит данные, сохраняет изображение,
    возвращает словарь с данными средства.

    :param url: url средства на сайте Золотого Яблока
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :return: dict
    """

    product_card_dict = get_product_dict(url=url)
    product_data_dict = get_product_data_dict(product_card_dict, image_dir_path)
    download_image(
        url=product_data_dict['Ссылка на изображение'],
        file_save_path=product_data_dict['Ссылка на изображение в базе'],
    )

    return product_data_dict
