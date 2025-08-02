""" Модуль для запуска парсера """

from time import sleep
from typing import Callable

from ga_parser.parser_v2.parser.parse import parse_product
from ga_parser.processing_data.excel.process_data import ExcelProcess
from ga_parser.utils.utils import (
    check_or_create_dir,
    path_to_universal,
    random_between, is_vpn_enabled,
)


def _process_product(
        products_for_parse: dict[str, tuple],
        excel_process: ExcelProcess,
        image_dir_path: str,
        base_delay: int,
        progress_callback: Callable | None = None,
):
    """
    Парсим средства по одному, записываем данные в таблицу, сохраняем изображение.
    Между запросами задержка.

    :param products_for_parse: словарь с ссылками на средства и
    кортежами ячеек (каждый кортеж ячеек это строка)
    :param excel_process: экземпляр объекта для работы с Excel книгой
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :param base_delay: базовая задержка в парсинге между запросами (в секундах)
    :param progress_callback: коллбэк для обновления прогресс бара
    """
    products_for_parse_len = len(products_for_parse)
    for index, product_link in enumerate(products_for_parse.keys(), 1):
        row = products_for_parse[product_link]
        product_data = parse_product(
            url=product_link,
            image_dir_path=image_dir_path,
        )

        excel_process.set_cells_values_in_row_by_title_from_dict(
            product_data=product_data,
            row=row
        )
        product = product_data.get('Название')
        print(f'Продукт "{product}" успешно спарсили🤙')
        excel_process.wb_save()

        # Вызов колбэка для обновления прогресс бара
        if progress_callback:
            progress_callback(index, products_for_parse_len)

        if index < products_for_parse_len:
            final_delay = random_between(base_delay)
            print(f'Ждём {final_delay} секунд...')
            sleep(final_delay)

    print('🚨 Не забудь проверить результаты парсинга в таблице 🚨')


def start_parser(
        table_path: str,
        ws_title: str,
        image_dir_path: str,
        base_delay: int,
        progress_callback=None,
) -> None:
    """
    Запускает процесс парсинга
    1. Создаём папку для изображений средств (если её нет)
    2. Получаем список с строками средств, которые надо спарсить
    3. Запускаем парсинг
    4. сохраняем книгу

    :param table_path: путь к файлу с книгой Excel
    :param ws_title: имя рабочего листа с средствами в книге Excel
    :param image_dir_path: базовый путь к папке, в которую сохранять изображения
    :param base_delay: базовая задержка в парсинге между запросами (в секундах)
    :param progress_callback: коллбэк для обновления прогресс бара
    """
    if is_vpn_enabled():
        print('❌ VPN включен, парсер не будет работать. Или золотое яблоко заблочил твой IP🤯 ')
        return

    check_or_create_dir(image_dir_path)

    excel_process = ExcelProcess(
        excel_file_path=path_to_universal(table_path),
        ws_title=ws_title
    )
    if excel_process.check_products_dublicates():
        print(
            (
                'Удали дубликаты в таблице средств для парсера, '
                'я выделил их красным ✋'
            )
        )
        return

    products_for_parse = excel_process.get_products_for_parse()
    _process_product(
        products_for_parse=products_for_parse,
        excel_process=excel_process,
        image_dir_path=image_dir_path,
        base_delay=base_delay,
        progress_callback=progress_callback,
    )
    excel_process.wb_close()
