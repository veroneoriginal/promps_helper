"""В этом модуле происходит формирование словарей из листов excel"""

from excel_process_data.process_data import ExcelManager



def load_data_tools_table(
        instance_excel: ExcelManager,
) -> dict:
    """
    Функция для создания общего словаря из листов Excel таблицы Средства

    :param instance_excel: объект класса ExcelManager, работающий с таблицей
    :return: словарь с загруженными данными
    """

    return {
        "Средства": instance_excel.load_info_about_products(ws_title='Средства'),
        "Тип": instance_excel.load_type_data(ws_title='Тип'),
        "Запрос": instance_excel.load_user_request(ws_title='Запрос'),
        "Задача": instance_excel.load_tasks_data(ws_title='Задача'),
        "Специалист": instance_excel.load_specialists_data(ws_title='Специалист'),
    }


def load_count_collections(
        instance_excel: ExcelManager,
) -> int:
    """
    Функция для получения количества подборок с листа Подборки таблицы Подборки

    :param instance_excel: объект класса ExcelManager, работающий с таблицей
    :return: словарь с загруженными данными
    """

    return instance_excel.count_empty_result()


def load_data_collection_table(
        instance_excel: ExcelManager,
) -> dict:
    """
    Функция для создания словаря c информацией о пользователе из листа Подборки таблицы Подборки

    :param instance_excel: объект класса ExcelManager, работающий с таблицей
    :return: словарь с загруженными данными
    """

    return {
        "Подборка": instance_excel.load_info_about_collection(ws_title='Подборки'),
    }
