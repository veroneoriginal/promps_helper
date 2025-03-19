import os
import shutil
from pathlib import Path


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
    print('transforming_dict_from_json_file')
    print(data)
    print()

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
