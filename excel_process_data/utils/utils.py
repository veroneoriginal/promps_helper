import copy
import hashlib
import json
import re
import datetime
# from pprint import pprint

from typing import Optional
from openpyxl.worksheet.worksheet import Worksheet


def extract_text(
        data: dict,
        main_key: str,
        description_key: str = "Описание",
) -> str:
    """
    Функция для извлечения нужных данных и объединения их в строку.

    :param data: словарь с данными; если не является словарём, то он просто преобразуется в строку
    :param main_key: ключ, значение которого должно быть в начале строки
    :param description_key: ключ для описания, значение которого добавляется
                            после основного (по умолчанию "Описание")

    :return: строка, объединяющая значения по ключам `main_key` и `description_key`,
             разделённые точкой и пробелом. Если ключи отсутствуют, возвращается пустая строка.
    """

    if isinstance(data, dict):
        return f"{data.get(main_key, '')}. {data.get(description_key, '')}".strip()

    return str(data)


def find_target_row_for_today_and_full_best_product(
        sheet: Worksheet,
        today_data: str,
        headers: dict,
) -> Optional[int] | None:
    """
    Функция определяет строку для вставки средств по текущей дате
    и свободной ячейке в столбце "Лучшее средство"

    :param sheet: активный лист из excel-документа
    :param headers: словарь с заголовками и нумерацией
    :param today_data: текущая дата

    :return: номер строки, в которую будет осуществляться запись
    """

    # Перебираем строки с конца
    for row in range(sheet.max_row, 1, -1):
        date_cell = sheet.cell(row=row, column=headers["Дата"]).value
        best_product = sheet.cell(row=row, column=headers["Лучшее средство"]).value

        if date_cell and best_product:
            if isinstance(date_cell, datetime.datetime):
                date_cell = date_cell.strftime("%d.%m.%Y")

            if date_cell == today_data:
                return row

    raise ValueError("Нет строки с сегодняшней датой и заполненным 'Лучшее средство'.")


def find_amount_funds(
        headers: dict,
) -> list:
    """
    Функция для поиска количества средств по заголовкам вида 'Средство <номер> Название'

    :param headers: словарь с заголовками и нумерацией
    :return: список с количеством средств, которые соответствуют заданному виду
    """

    pattern = re.compile(r"Средство (\d+) Название")
    product_numbers = []

    for header in headers:
        # Проверка соответствия заголовка шаблону
        match = pattern.fullmatch(str(header).strip())
        if match:
            # Извлекаем номер и добавляем в список
            product_numbers.append(int(match.group(1)))

    return product_numbers


def function_for_forming_dict_with_correlation(
        sheet: Worksheet,
        product_numbers: list,
        target_row: int,
        headers: dict,
        best_mean: str,
) -> dict:
    """
    Функция для составления словаря, где ключами являются названия средств,
    а значениями - словари с плюсами и минусами этих средств.

    :param sheet: активный лист из excel-документа
    :param product_numbers: список с нумерацией средств
    :param target_row: строка, в которой осуществляется работа
    :param headers: словарь с заголовками и нумерацией
    :param best_mean: название лучшего средства

    :return: словарь со средствами и их плюсами и минусами
    """

    selection_dict = {}

    for i in product_numbers:
        name = sheet.cell(row=target_row, column=headers.get(f"Средство {i} Название")).value
        if not name:
            continue

        plus = sheet.cell(row=target_row, column=headers.get(f"Средство {i} ПЛЮСЫ")).value
        minus = sheet.cell(row=target_row, column=headers.get(f"Средство {i} МИНУСЫ")).value

        selection_dict[name] = {
            "Плюсы": plus,
            "Минусы": minus,
            "Лучшее средство": (name == best_mean)
        }

    return selection_dict


def converting_lists(
        products: list,
) -> list:
    """
    Функция для преобразования списка списков в 1 единый список

    :param products: список списков со средствами
    :return: список со средствами
    """
    flat_products = []  # создаём пустой список

    for sublist in products:  # проходим по каждому вложенному списку
        for item in sublist:  # проходим по каждому элементу вложенного списка
            flat_products.append(item)  # добавляем элемент в итоговый список

    return flat_products


def counting_hash(
        data: dict,
) -> str:
    """
    Функция для подсчета хеша текущей поборки

    :param data: словарь, в котором содержится текущая подборка
    :return: хеш текущей подборки
    """

    # Создаем копию словаря с данными по текущей подборке, чтобы не изменять оригинал
    data_copy = copy.deepcopy(data)

    # привожу к нормальному виду "Средства"
    # получаю строку
    edit_products = data_copy['Средства'].replace("«", '"').replace("»", '"').replace('\n', '')

    # Преобразуем строку словаря в список значений
    edit_products = list(json.loads(edit_products).values())

    if data['Задача'] == "Лучшая пара":
        convert_products = converting_lists(products=edit_products)
        # Сортируем и приводим к кортежу
        data_copy['Средства'] = tuple(convert_products)
    else:
        # Сортируем и приводим к кортежу
        data_copy['Средства'] = tuple(edit_products)

    # привожу к нормальному виду "Тип"
    edit_type = data['Тип']
    types_list = edit_type.split(',')
    # pylint: disable=R1728 consider-using-generator
    data_copy['Тип'] = tuple([type_elem.strip() for type_elem in types_list])

    data_copy['Возраст'] = str(data_copy['Возраст'])

    list_for_hash = []
    for key, value in data_copy.items():
        if key not in ("Содержимое", "Лучший вариант", "Итог", "Хеш"):
            list_for_hash.append(value)

    # Создаём новый список, "разворачивая" кортежи
    new_list = []
    for item in list_for_hash:
        if isinstance(item, tuple):
            new_list.extend(item)  # Добавляем элементы кортежа напрямую
        else:
            new_list.append(item)  # Добавляем остальные элементы как есть

    final_tuple = tuple(sorted(new_list))

    final_str = str(final_tuple).encode()

    return hashlib.sha256(final_str).hexdigest()
