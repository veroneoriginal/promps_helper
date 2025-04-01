""" Логика парсера второй версии"""

from ga_parser.parser_v2.parser.generation_product_data import get_product_data_dict
from ga_parser.utils.requests_funcs import get_page_v2
from ga_parser.utils.utils import (
    download_image,
)


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

    html = get_page_v2(url=url)
    product_data_dict = get_product_data_dict(html=html, image_dir_path=image_dir_path)

    download_image(
        url=product_data_dict['Ссылка на изображение'],
        file_save_path=product_data_dict['Путь для сохранения изображения'],
    )

    return product_data_dict
