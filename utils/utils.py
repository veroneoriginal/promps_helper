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
