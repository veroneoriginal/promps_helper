# pylint: disable=E0611: no-name-in-module
from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    get_brand_line_path,
    get_pdf_doc_sizes,
    get_brand_line_sizes,
    get_pdf_flowables,
    get_pdf_page_templates,
)


def format_product_filename(
        product_title: str,
        path_to_output_folder_pdf_file: str,
) -> Path:
    """
    Возвращает полный путь для сохранения файла .pdf

    :param path_to_output_folder_pdf_file: путь (Path) к папке для сохранения PDF.
    :param product_title: наименование средства

    :return: полный путь к файлу PDF
    """

    output_folder_pdf = Path(path_to_output_folder_pdf_file)
    safe_filename = product_title.replace(" ", "_").replace("/", "_").lower() + ".pdf"

    return output_folder_pdf / safe_filename


def best_product_get_brand_line_path(
        task: str,
        value: bool
):
    """
    Возвращает путь к файлу с нужной бренд-линией для нанесения
    на PDF для задачи "Лучшее средство"
    :param task: код задачи
    :param value: данные
    :return: путь до файла с бренд-линией
    """
    colors = {
        True: 'Цвет_1',
        False: 'Цвет_2',
    }

    return get_brand_line_path(task, colors[value])


def best_product_calc_base_price_ratio(
        product: dict,
) -> str:
    """
    Готовит строку 'Количество мера / цена'
    Например: '190 мл / 1612 р.'

    :param product: словарь с информацией по одному средству
    :return: str
    """

    return (
        f'{product.get("Количество меры (число)")} '
        f'{product.get("Юниты меры (мл/шт)")} / {product.get("Стоимость руб")} рублей'
    )


def best_product_task_main(
        collection_data: dict,
        info_data: dict,
        selection_result: dict,
        path_to_output_folder_pdf_file: str,
) -> dict:
    """
    Задача "Лучшее средство"

    :param collection_data: данные подборки
    :param info_data: данные с всеми средствами, врачами и т.д.
    :param selection_result: данные с результатом нейронки по подборке
    :param path_to_output_folder_pdf_file: путь к папке для сохранения pdf-файлов

    :return: список словарей с данными по средствам, готовыми к передаче в PDFCreator
    """
    # создаем список
    products_data = []

    # формируем список из словарей с данными по средствам

    for key, value in selection_result.items():
        if key.startswith('product_'):
            products_data.append(
                {
                    'Название средства': value['title'],
                    'Плюсы': value['plus'],
                    'Минусы': value['minus'],
                    'Количество мера / цена': best_product_calc_base_price_ratio(
                        info_data[value['title']]
                    ),
                    'Путь к изображению средства': Path(
                        info_data[value['title']]['Ссылка на изображение в базе']),
                    'Путь к изображению бренд-линии': Path(best_product_get_brand_line_path(
                        task=collection_data['Задача'],
                        value=value['best_product']
                    )
                    ),
                    'Размеры бренд-линии': get_brand_line_sizes(
                        task=collection_data['Задача'],
                    ),
                    'Путь для сохранения pdf-файла': format_product_filename(
                        product_title=value['title'],
                        path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
                    ),
                    'Размеры документа': get_pdf_doc_sizes(
                        task=collection_data['Задача']
                    ),
                    'Элементы и стили': get_pdf_flowables(
                        task=collection_data['Задача']
                    ),
                    'Шаблоны страниц с фреймами': get_pdf_page_templates(
                        task=collection_data['Задача']
                    ),
                    'Тип продукта': info_data[value['title']]['Тип продукта'].upper(),
                }
            )

    return {
        'Задача': collection_data['Задача'],
        'Категория': collection_data['Категория'],
        'Данные': products_data,
    }
