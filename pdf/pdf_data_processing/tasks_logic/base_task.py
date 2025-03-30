# pylint: disable=E0611: no-name-in-module
from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    calc_base_price_ratio, extract_product_name, capitalize_first_letter,
)


def get_base_info_by_product(
        info_data: dict,
        product_name: str,
        product_article: str,
) -> dict:
    """
    Получает базовые данные по средству

    :param info_data: данные с всеми средствами, врачами и т.д.
    :param product_name: название средства
    :param product_article: Артикул средства в Золотом Яблоке

    """
    list_name = 'Средства'
    product_data = info_data[list_name][product_name][product_article]

    return {
        # одинаково для всех средств:
        'Название средства': extract_product_name(product_name),

        'Количество мера / цена': calc_base_price_ratio(
            product_data
        ),
        'Путь к изображению средства': Path(
            product_data['Ссылка на изображение в базе']),
        'Тип продукта': capitalize_first_letter(
            product_data['Тип продукта подробно']
            or product_data['Тип продукта']
        ),
        'Артикул': f'артикул: {product_data["Артикул в Золотом Яблоке"]}'
    }
