# pylint: disable=E0611: no-name-in-module
from copy import deepcopy
from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    calc_base_price_ratio,
    get_brand_line_sizes,
    format_product_filename,
    get_pdf_doc_sizes,
    get_pdf_flowables,
    get_pdf_page_templates,
    mapping_keys_to_rus,
)


def process_products_common(
        collection_data: dict,
        info_data: dict,
        all_products_data: list,
        path_to_output_folder_pdf_file: str,
        build_product_data_func: callable,
) -> dict:
    """
    Общая логика подготовки данных по средствам.

    :param collection_data: данные подборки
    :param info_data: данные по средствам
    :param all_products_data: список словарей средств
    :param path_to_output_folder_pdf_file: путь к папке PDF
    :param build_product_data_func: функция для построения специфичных данных средства
    :return: словарь с итоговыми данными
    """
    final_products_data = []

    for product in all_products_data:
        rus_product_data_dict = mapping_keys_to_rus(data=deepcopy(product))
        product_name = rus_product_data_dict['Название средства']
        # Подготовка базовых данных по средству
        base_product_data = _get_base_info_by_product(
            collection_data=collection_data,
            info_data=info_data,
            product_name=product_name,
            path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
        )
        # Подготовка специфических данных по средству
        specific_data = build_product_data_func(
            collection_data=collection_data,
            info_data=info_data,
            rus_product_data_dict=rus_product_data_dict,
            product_name=product_name,
        )

        base_product_data.update(specific_data)
        final_products_data.append(base_product_data)

    return {
        'Задача': collection_data['Задача'],
        'Категория': collection_data['Категория'],
        'Данные': final_products_data,
    }


def _get_base_info_by_product(
        collection_data: dict,
        info_data: dict,
        product_name: str,
        path_to_output_folder_pdf_file: str,
) -> dict:
    """
    Получает базовые данные по средству

    :param collection_data: данные подборки
    :param info_data: данные с всеми средствами, врачами и т.д.
    :param product_name: название средства
    :param path_to_output_folder_pdf_file: путь к папке для сохранения pdf-файлов

    """
    list_name = 'Средства'

    return {
        # одинаково для всех средств:
        'Название средства': product_name,

        'Количество мера / цена': calc_base_price_ratio(
            info_data[list_name][product_name]
        ),
        'Путь к изображению средства': Path(
            info_data[list_name][product_name]['Ссылка на изображение в базе']),
        'Размеры бренд-линии': get_brand_line_sizes(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
        ),
        'Путь для сохранения pdf-файла': format_product_filename(
            product_title=product_name,
            path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
        ),
        'Размеры документа': get_pdf_doc_sizes(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
        ),
        'Элементы и стили': get_pdf_flowables(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
        ),
        'Шаблоны страниц с фреймами': get_pdf_page_templates(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
        ),
        'Тип продукта': info_data[list_name][product_name]['Тип продукта'],
    }
