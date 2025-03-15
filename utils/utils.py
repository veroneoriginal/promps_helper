import os
import shutil
from pathlib import Path


def split_and_clean_type(
        symbol: str,
        type_of_need: str | tuple,
) -> list:
    """
    Метод для обработки строки (значения, взятого из ячейки):
    если в строке есть определенный символ, разделяет и очищает значения,
    если символа нет, возвращает список с одним очищенным значением.

    :param symbol: символ, по которому осуществляется сплит
    :param type_of_need: строка или кортеж со значениями, например "B2, B1" или "B2"
    :return: список очищенных значений, например ['B2', 'B1'] или ['B2']
    """

    if isinstance(type_of_need, tuple):
        # Если передан кортеж, сразу превращаем его в список строк
        return [str(value).strip() for value in type_of_need if value]

    if isinstance(type_of_need, str):
        # Убираем лишние пробелы с начала и конца строки
        type_need = type_of_need.strip()

        # Проверяем, есть ли символ в строке
        if symbol in type_need:
            # Если есть символ, разделяем и очищаем значения
            values = type_need.split(symbol)
            return [value.strip() for value in values if value.strip()]

        # Если символа нет, возвращаем список с одним очищенным значением
        return [type_need] if type_need else []

    return []


def decrypting_data_from_cell(
        data: dict,
        data_collection: dict,
        category: str,
) -> str:
    """
    Метод для расшифровки данных из блоков Тип, Запрос

    :param data: словарь со всеми данными
    :param data_collection: словарь с подборкой
    :param category: категория, с который работаем
    :return: расшифрованная строка
    """

    # получение строки с содержимым, которое было в ячейке ТИП
    body_part_type = data_collection[category]

    # формирование из строки списка отдельных элементов
    list_body_part_type = split_and_clean_type(type_of_need=body_part_type, symbol=",")

    # формирование списка словарей с расшифрованными значениями
    params = []

    # расшифровывание кодов и добавление в этот новый список
    for element in list_body_part_type:
        params.append(data[category][element])

    # преобразование списка словарей в предложения
    sentences = []
    for item in params:
        sentence = f"{item['Область применения']}: {item['Суть']}. {item['Описание']}"
        sentences.append(sentence)

    return ' '.join(sentences)


def decrypting_info_from_cell(
        data: dict,
        data_collection: dict,
        category: str,
) -> str:
    """
    Метод для расшифровки данных из блоков Задача, Специалист

    :param data: словарь со всеми данными
    :param data_collection: словарь с подборкой
    :param category: категория, с который работаем
    :return: расшифрованная строка
    """

    # получение строки с содержимым, которое было в ячейке
    body_part_type = data_collection[category]

    # обращение по полученному коду к основному словарю с содержимым
    dict_with_full_info = data[category][body_part_type]

    return f"{dict_with_full_info['Описание']}"


def conversion_products(
        cosmetic_products: dict,
) -> str:
    """
    Метод для преобразования блока со средствами, их составами и типами в читабельный текст

    :param cosmetic_products: принимает словарь со средствами, их составом и типом
    :return: возвращает читаемую строку для промпта
    """

    list_cosmetic_products = []

    for key, value in cosmetic_products.items():
        list_cosmetic_products.append(
            f"Средство №{value['Номер']} - {key}. "
            f"Состав: {value['Состав']}. Тип продукта: {value['Тип продукта']}. ")

    # строка, которая объединяет инфо о всех сред-х в единый текст блок с переносами строк
    return "\n".join(list_cosmetic_products)


def decrypting_info_from_products(
        data: dict,
        data_collection: dict,
        category: str,
) -> str:
    """
    Метод для расшифровки данных из блока Средства

    :param data: словарь со всеми данными
    :param data_collection: словарь с подборкой
    :param category: категория, с который работаем
    :return: словарь со средствами, их типом и составом
    """

    # получение строки с содержимым, которое было в ячейке
    products_in_cell = data_collection[category]

    # формирование из строки списка отдельных элементов
    list_products = split_and_clean_type(type_of_need=products_in_cell, symbol="&&&")

    # формируем словарь
    products_full_info = {}
    for number, product in enumerate(list_products):
        products_full_info[product] = {
            "Номер": number + 1,
            "Тип продукта": data[category][product]["Тип продукта"],
            "Состав": data[category][product]["Состав"],
        }

    # преобразование словаря со средствами в строку
    return conversion_products(cosmetic_products=products_full_info)


def decrypting_data_from_current_collection(
        data_tools: dict,
        data_collection: dict,
) -> dict:
    """
    Функция для расшифровки данных из словаря текущей подборки

    :param data_tools: словарь с информацией о средствах, типах и прочем
    :param data_collection: словарь с данными текущей подборки
    :return: словарь с расшифрованными данными по текущей подборке
    """

    # расшифровка данных по ключу Тип
    data_collection['Тип'] = decrypting_data_from_cell(
        data=data_tools,
        data_collection=data_collection,
        category="Тип",
    )

    # расшифровка данных по ключу Запрос
    data_collection["Запрос"] = decrypting_data_from_cell(
        data=data_tools,
        data_collection=data_collection,
        category="Запрос",
    )

    # расшифровка данных по ключу Задача - ее содержимое пойдет в settings
    data_collection["Задача"] = decrypting_info_from_cell(
        data=data_tools,
        data_collection=data_collection,
        category="Задача",
    )

    # расшифровка данных по ключу Специалист - ее содержимое пойдет в system
    data_collection["Специалист"] = decrypting_info_from_cell(
        data=data_tools,
        data_collection=data_collection,
        category="Специалист",
    )

    # расшифровка средств
    data_collection["Средства"] = decrypting_info_from_products(
        data=data_tools,
        data_collection=data_collection,
        category="Средства",
    )

    return data_collection


def copy_jpg_files(
        where_copy_from: Path,
        where_copy_to: Path,
        file_extension: str = '.jpg',
) -> None:
    """
    Функция для копирования JPG файлов из одной папки в другую

    :param where_copy_from: путь до папки, из которой копируем (откуда)
    :param where_copy_to: путь до папки, в которую копируем (куда)
    :param file_extension: расширение файла
    :return: None
    """

    # Получаем список всех JPG файлов в исходной папке
    jpg_files = []
    for file in os.listdir(where_copy_from):
        if file.lower().endswith(file_extension):
            jpg_files.append(file)

    # Копируем файлы в целевую папку
    for jpg_file in jpg_files:
        # Получаем полный путь к исходному файлу
        source_path = os.path.join(where_copy_from, jpg_file)

        # Аналогично создаём полный путь к целевому файлу в папке назначения
        dest_path = os.path.join(where_copy_to, jpg_file)

        # копируем файл из исходного места в желаемое
        shutil.copy2(source_path, dest_path)


def transforming_dict_from_json_file(
        data: dict,
) -> dict:
    """
    Функция для формирования нового словаря со средствами на основе json-фaйла,
    где ключами будут названия средств.

    :param data: словарь, сформированный из json-фaйла
    :return: словарь, в котором ключами являются названия средств
    """

    # формирую словарь со средствами из json-a, чтобы его дальше дополнить
    transformed_dict = {}

    # проходим по значениям json-словаря
    for product_info in data.values():
        # Извлекаем заголовок (название продукта)
        title = product_info['title']

        # Создаем новый словарь без ключа 'title'
        product_data = {}
        for key, value in product_info.items():
            # Пропускаем ключ 'title'
            if key != 'title':
                # Добавляем остальные данные
                product_data[key] = value

            # Добавляем в новый словарь с ключом-названием
            transformed_dict[title] = product_data

    return transformed_dict


def add_keys_from_another_dict_to_one_dict(
        base_dict: dict,
        transform_dict: dict,
        list_keys: list,
) -> dict:
    """
    Функция для дополнения одного словаря ключами из другого

    :param base_dict: базовый словарь, из которого берем значения по ключам
    :param transform_dict: словарь, который дополняем
    :param list_keys: список ключей, которыми нужно дополнить transform_dict
    :return: дополненный словарь
    """

    for product_title, product_data in transform_dict.items():
        # Перебираем только нужные ключи
        for key in list_keys:
            # Добавляем только нужные данные
            product_data[key] = base_dict[product_title][key]

    return transform_dict
