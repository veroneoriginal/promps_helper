# pylint: disable=E0611: no-name-in-module
from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    calc_base_price_ratio, extract_product_name, capitalize_first_letter,
)


def get_base_info_by_product(
        info_data: dict,
        product_name: str,
) -> dict:
    """
    Получает базовые данные по средству

    :param info_data: данные с всеми средствами, врачами и т.д.
    :param product_name: название средства

    """
    list_name = 'Средства'
    product_description = info_data[list_name][product_name]['Тип продукта']
    delailed_product_description = info_data[list_name][product_name]['Тип продукта подробно']

    return {
        # одинаково для всех средств:
        'Название средства': extract_product_name(product_name),

        'Количество мера / цена': calc_base_price_ratio(
            info_data[list_name][product_name]
        ),
        'Путь к изображению средства': Path(
            info_data[list_name][product_name]['Ссылка на изображение в базе']),
        'Тип продукта': capitalize_first_letter(delailed_product_description or product_description),
        'Артикул': f'артикул: {info_data[list_name][product_name]["Артикул в Золотом Яблоке"]}'
    }
