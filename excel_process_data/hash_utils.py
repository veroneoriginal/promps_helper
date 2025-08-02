import copy
import hashlib

from control_manager.utils import is_collection_without_user_parameters
from excel_process_data.process_data import ExcelManager


def is_hash_unique(
        file_path_collection: str,
        hash_collection: str,
        row_number: int,
) -> str | None:
    """
    Проверяет хеш подборки на уникальность.
    Сначала проверяет совпадения в новых подборках, потом в архиве.
    Возвращает номер строки, если подборка не уникальна

    :param file_path_collection: путь до таблицы с подборками
    :param hash_collection: хеш подборки
    :param row_number: нмоер строки с проверяемой подборкой
    """
    # проверяет совпадения в новых подборках
    un_unique_in_new_collection = check_hash_in_collection(
        ws_title='Подборки',
        file_path_collection=file_path_collection,
        hash_collection=hash_collection,
    )
    if un_unique_in_new_collection:
        excel_manager = ExcelManager(file_path=file_path_collection)
        excel_manager.fill_row_color(
            ws_title='Подборки',
            row_nums=(un_unique_in_new_collection, row_number),
        )
        excel_manager.save_wb()
        excel_manager.close_wb()
        return (
            f'При проверке хеша подборки в строке {row_number} '
            f'⚠ нашли такой же хеш в новых подборках ⚠'
            f' в строке {un_unique_in_new_collection} и выделили её красным'
        )
    # проверяет совпадения в архивных подборках
    un_unique_in_arhiv_collection = check_hash_in_collection(
        ws_title='Архив',
        file_path_collection=file_path_collection,
        hash_collection=hash_collection,
    )
    if un_unique_in_arhiv_collection:
        excel_manager = ExcelManager(file_path=file_path_collection)
        excel_manager.fill_row_color(
            ws_title='Подборки',
            row_nums=(row_number,),
        )
        excel_manager.fill_row_color(
            ws_title='Архив',
            row_nums=(un_unique_in_arhiv_collection,),
        )
        excel_manager.save_wb()
        excel_manager.close_wb()
        return (
            f'При проверке хеша подборки в строке {row_number} '
            f'⚠ нашли такой же хеш в архиве подборок ⚠'
            f' в строке {un_unique_in_arhiv_collection} и выделили её красным'
        )

    return None


def check_hash_in_collection(
        ws_title: str,
        file_path_collection: str,
        hash_collection: str,
):
    """
    Проверяет хеш на уникальность.
    Кортеж хешей формирует из столбца "Хеш" из указанного листа
    :param file_path_collection: путь до книги эксель
    :param ws_title: имя листа
    :param hash_collection: хеш подборки
    """

    excel_manager = ExcelManager(file_path=file_path_collection)

    all_collection_hash = excel_manager.get_column_values(
        ws_title=ws_title,
        column_title='Хеш'
    )
    un_unique_row_number = all_collection_hash.get(hash_collection, None)
    excel_manager.close_wb()
    return un_unique_row_number


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
    if not is_collection_without_user_parameters(collection_data=data):
        # приводим к кортежу
        data_copy['Средства'] = get_values(data_copy['Средства'])
        # приводим к спискам
        data_copy['Тип'] = normalize_list_string(data['Тип'])
        data_copy['Запрос'] = normalize_list_string(data['Запрос'])

    # Сбор значений для хеша
    include_keys = {"Пол", "Возраст", "Тип", "Запрос", "Задача", "Специалист", "Средства"}
    list_for_hash = []
    for key, value in data_copy.items():
        if key not in include_keys:
            continue
        if isinstance(value, (list, tuple)):
            # Разворачиваем список или кортеж
            list_for_hash.extend(str(v).lower().strip() for v in value)
        else:
            list_for_hash.append(str(value).lower().strip())

    # Сортировка и хеширование
    final_list = sorted(list_for_hash)
    final_str = ','.join(final_list).encode("utf-8")
    return hashlib.sha256(final_str).hexdigest()


def normalize_list_string(value: str) -> list[str]:
    return [item.strip().lower() for item in value.split(',') if item.strip()]


def get_values(
        data,
        list_with_product=None,
) -> list:
    """
    Рекурсивная функция для извлечения всех значений из словаря любой вложенности.

    - Функция проходит по каждому элементу словаря.
    - Если значение элемента является ещё одним словарём (dict),
    функция вызывает сама себя (рекурсия) и продолжает обход на более глубоком уровне.
    - Если значение элемента является кортежем (tuple) - превращаем в список, идём по элементам
    и если элемент словарь - снова вызываем рекурсию, если нет - добавляем в общий список,
    функция вызывает сама себя (рекурсия) и продолжает обход на более глубоком уровне.
    - Если значение не является словарём (например, строка, число и т.д.),
    оно добавляется в результирующий список.

    :param data: словарь, из которого необходимо получить все значения.
    Может содержать вложенные словари.
    :param list_with_product: список, в который будут добавляться найденные значения.
    Если не передан, создаётся новый пустой список.

    :return: список со средствами, забранными из вложенной структуры
    """
    if list_with_product is None:
        list_with_product = []

    for value in data.values():
        if isinstance(value, dict):
            get_values(value, list_with_product)
        elif isinstance(value, tuple):
            for item in value:
                if isinstance(item, dict):
                    get_values(item, list_with_product)
                elif isinstance(item, str):
                    list_with_product.append(item.lower())
                else:
                    list_with_product.append(item)
        elif isinstance(value, str):
            list_with_product.append(value.lower())
        else:
            list_with_product.append(value)

    return list_with_product
