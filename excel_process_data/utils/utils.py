import ast
import copy
import hashlib

import re
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


def get_values(
        data,
        list_with_product=None,
) -> list:
    """
    Рекурсивная функция для извлечения всех значений из словаря любой вложенности.

    - Функция проходит по каждому элементу словаря.
    - Если значение элемента является ещё одним словарём (dict),
    функция вызывает сама себя (рекурсия) и продолжает обход на более глубоком уровне.
    - Если значение не является словарём (например, строка, число и т.д.),
    оно добавляется в результирующий список.

    :param data: словарь, из которого необходимо получить все значения.
    Может содержать вложенные словари.
    :param list_with_product: список, в который будут добавляться найденные значения.
    Если не передан, создаётся новый пустой список.

    :return: список со средствами, забранными из сложенной структуры
    """
    if list_with_product is None:
        list_with_product = []

    for _, value in data.items():
        if isinstance(value, dict):
            # Рекурсивно спускаемся на уровень ниже
            get_values(value, list_with_product)
        else:
            # Добавляем найденное значение в список
            list_with_product.append(value)

    return list_with_product


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

    # pylint: disable=C0301 line-too-long
    # привожу к нормальному виду "Средства" / получаю строку
    edit_products = data_copy['Средства'].replace("«", '"').replace("»", '"').replace('\n', '').lower()

    # Преобразуем строку в словарь
    edit_products_dict = ast.literal_eval(edit_products)

    # приводим к кортежу
    data_copy['Средства'] = get_values(edit_products_dict)

    # привожу к нормальному виду "Тип"
    edit_type_list = data['Тип'].split(',')
    data_copy['Тип'] = [type_elem.strip() for type_elem in edit_type_list]

    data_copy['Возраст'] = str(data_copy['Возраст'])

    list_for_hash = []
    for key, value in data_copy.items():
        if key not in ("Содержимое", "Лучший вариант", "Путь", "Хеш"):
            if isinstance(value, (list, tuple)):
                list_for_hash.extend(value)  # Разворачиваем список или кортеж
            else:
                list_for_hash.append(value)

    # Сортируем список для консистентности хеша
    final_list = sorted(list_for_hash)

    # Хэшируем как строку
    final_str = str(final_list).encode()

    return hashlib.sha256(final_str).hexdigest()
