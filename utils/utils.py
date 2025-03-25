import os
import shutil
import json
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


def save_to_json_file(
        path_to_file: str,
        what_save: dict,
) -> None:
    """
    Метод для сохранения json-файлов

    :param path_to_file: путь к файлу внутри папки, куда идет сохранение
    :param what_save: объект сохранения (что сохраняем)
    :return None: ничего не возвращает, просто сохраняет и всё
    """

    # Сохраняем JSON
    with open(path_to_file, 'w', encoding='utf-8') as file:
        json.dump(what_save, file, ensure_ascii=False, indent=4)


def save_dif_extension_to_file(
        path_to_file: str,
        what_save: str,
) -> None:
    """
    Метод для сохранения файлов разного расширения

    :param path_to_file: путь к файлу внутри папки, куда идет сохранение
    :param what_save: объект сохранения (что сохраняем)
    :return None: ничего не возвращает, просто сохраняет и всё
    """

    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write(what_save)


def save_file_in_process_work(
        what_save: dict | str,
        path_to_folder: str,
        file_name: str,
        file_extension: str,
) -> None:
    """
    Метод для сохранения json-схемы / промпта или чего-то еще

    :param what_save: объект, который нужно сохранить
    :param path_to_folder: путь к нужной папке из словаря с путями
    :param file_name: название файла, в который сохраняем инфу
    :param file_extension: расширение файла, в котором сохраняется информация
    :return: None
    """

    # Создаём путь к файлу внутри этой папки
    path_to_file = os.path.join(path_to_folder, f'{file_name}{file_extension}')

    if file_extension == ".json":
        save_to_json_file(
            path_to_file=path_to_file,
            what_save=what_save,
        )
    else:
        save_dif_extension_to_file(
            path_to_file=path_to_file,
            what_save=what_save,
        )
