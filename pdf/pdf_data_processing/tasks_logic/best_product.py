# pylint: disable=E0611: no-name-in-module
from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    get_brand_line_path,
)


def best_product_get_brand_line_path(
        task: str,
        category: str,
        value: bool
):
    """
    Возвращает путь к файлу с нужной бренд-линией для нанесения
    на PDF для задачи "Лучшее средство"
    :param task: код задачи
    :param category: категория подборки
    :param value: данные
    :return: путь до файла с бренд-линией
    """
    colors = {
        True: 'Цвет_1',
        False: 'Цвет_2',
    }

    return get_brand_line_path(
        task=task,
        category=category,
        brand_line_color=colors[value],
    )


# pylint: disable=W0613 unused-argument
def best_product_task_main(
        collection_data: dict,
        info_data: dict,
        rus_product_data_dict: dict,
        product_name: str,
) -> dict:
    """
    Задача "Лучшее средство"

    :param collection_data: данные подборки
    :param info_data: данные с всеми средствами, врачами и т.д.
    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :param product_name: наименование средства

    :return: словарь с специфичными данными по средству по задаче
    """

    return {  # отличается:
        'Плюсы': rus_product_data_dict['Плюсы'],
        'Минусы': rus_product_data_dict['Минусы'],
        'Путь к изображению бренд-линии': Path(best_product_get_brand_line_path(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
            value=rus_product_data_dict['Лучшее средство'],
        )
        )
    }
