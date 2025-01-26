""" Модуль для запуска парсера """

from pathlib import Path
from time import sleep

from ga_parser.parser.parse import parse_product
from ga_parser.processing_data.excel.process_data import ExcelProcess
from ga_parser.utils.utils import (
    check_or_create_dir,
    path_to_universal,
    random_between,
)


def _process_product(
        products_for_parse: dict[str, tuple],
        excel_process: ExcelProcess,
        image_dir_path: Path,
        base_delay: int,
):
    """
    Парсим средства по одному, записываем данные в таблицу, сохраняем изображение.
    Между запросами задержка.

    :param products_for_parse: словарь с ссылками на средства и
    кортежами ячеек (каждый кортеж ячеек это строка)
    :param excel_process: экземпляр объекта для работы с Excel книгой
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :param base_delay: базовая задержка в парсинге между запросами (в секундах)
    """
    products_for_parse_len = len(products_for_parse)
    for index, product_link in enumerate(products_for_parse.keys(), 0):
        row = products_for_parse[product_link]
        product_data = parse_product(
            url=product_link,
            image_dir_path=image_dir_path,
        )

        excel_process.set_cells_values_in_row_by_title_from_dict(
            product_data=product_data,
            row=row
        )
        if index + 1 < products_for_parse_len:
            final_delay = random_between(base_delay)
            print(f'Ждём {final_delay} секунд...')
            sleep(final_delay)


def start_parser(
        table_path: str,
        ws_title: str,
        image_dir_path: str,
        base_delay: int,
) -> None:
    """
    Запускает процесс парсинга
    1. Создаём папку для изображений средств (если её нет)
    1. Получаем список с строками средств, которые надо спарсить
    2. Запускаем парсинг
    3. сохраняем книгу

    :param table_path: путь к файлу с книгой Excel
    :param ws_title: имя рабочего листа с средствами в книге Excel
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :param base_delay: базовая задержка в парсинге между запросами (в секундах)
    """
    check_or_create_dir(image_dir_path)

    excel_process = ExcelProcess(
        excel_file_path=path_to_universal(table_path),
        ws_title=ws_title
    )
    products_for_parse = excel_process.get_products_for_parse()
    _process_product(
        products_for_parse=products_for_parse,
        excel_process=excel_process,
        image_dir_path=path_to_universal(image_dir_path),
        base_delay=base_delay,
    )
    excel_process.wb_close()


if __name__ == '__main__':
    start_parser(
        table_path='../00_base/00_Средства.xlsx',
        ws_title='Средства',
        image_dir_path='../00_base/01_products/00_img/',
        base_delay=10,
    )
