# pylint: disable=E0611: no-name-in-module
import shutil
from pathlib import Path

import re

import emoji

from source.structure_folders import EMOJI_IMAGE_DIR, SUBSCRIBE_GREEN_VERTICAL_IMAGE_PATH, \
    SUBSCRIBE_ORANGE_VERTICAL_IMAGE_PATH


def copy_image_if_needed(
        folder_path: str | Path,
        task: str,
) -> None:
    """
    Копирует изображение в папку, если в ней сейчас 3 или 5 изображений.

    :param folder_path: путь к папке
    :param task: задача подборки
    """
    folder = Path(folder_path)

    green = {
        'Разбор состава одного средства': SUBSCRIBE_GREEN_VERTICAL_IMAGE_PATH,
        'Подробный анализ состава': SUBSCRIBE_ORANGE_VERTICAL_IMAGE_PATH,
        'Лучшее сочетание': SUBSCRIBE_GREEN_VERTICAL_IMAGE_PATH,
        'Лучшее средство': SUBSCRIBE_GREEN_VERTICAL_IMAGE_PATH,
    }

    image_path = green.get(task)

    if image_path is None:
        return

    image = Path(image_path)

    PAGE_COUNT_FOR_COPY = (3, 5, 7, 8)

    # Считаем только изображения (фильтр по расширениям)
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    images_in_folder = [f for f in folder.iterdir() if f.suffix.lower() in image_exts]

    if len(images_in_folder) in PAGE_COUNT_FOR_COPY:
        target_path = folder / image.name
        shutil.copy(image, target_path)


def _get_pdf_file_paths(
        input_data: list,
        path_to_output_folder_jpg_file: str,
) -> dict:
    """
    Возвращает словарь вида:
    {путь к PDF-файлу: {size:  размеры документа, jpg_file_name: путь для сохранения jpg})
    :param input_data: список с словарями данных по каждому средству
    :param path_to_output_folder_jpg_file: путь к папке для сохранения JPG-файлов

    :return: словарь с путями и размерами
    """
    output_data = {}
    output_folder = Path(path_to_output_folder_jpg_file)

    for product in input_data:
        pdf_file_path = Path(product.get('Путь для сохранения pdf-файла'))
        size = product.get('Размеры документа')

        # Меняем расширение .pdf → .jpg
        jpg_file_name = pdf_file_path.with_suffix(".jpg").name

        output_data[pdf_file_path] = {
            "size": size,
            "jpg_file_name": output_folder / jpg_file_name,
        }

    return output_data


def convert_markdown_to_html(text: str) -> str:
    """ Заменяет **жирный** → <b>жирный</b> """
    return re.sub(r'\*\*(.+?)\*\*', r'<font name="Montserrat-Bold">\1</font>', text)


def unicode_to_twemoji_codepoint(char: str) -> str:
    """ Преобразует emoji в codepoint-строку, исключая FE0F, если надо """

    codepoints = [f"{ord(c):x}" for c in char]

    # Если последний элемент FE0F — пробуем без него
    if codepoints[-1] == 'fe0f':
        test_path = EMOJI_IMAGE_DIR / f"{'-'.join(codepoints[:-1])}.png"
        if test_path.exists():
            codepoints = codepoints[:-1]

    return '-'.join(codepoints)


def replace_emoji_html(text: str, size=16) -> str:
    """ Заменяет emoji символы на <img> с реальным путем, понятным ReportLab. """
    new_text = ''
    last_index = 0

    for e in emoji.emoji_list(text):
        start = e['match_start']
        end = e['match_end']
        emoji_char = text[start:end]
        codepoint = unicode_to_twemoji_codepoint(emoji_char)

        # Путь для ReportLab должен быть читаемым на диске
        img_path = EMOJI_IMAGE_DIR / f"{codepoint}.png"
        img_path_str = img_path.resolve().as_posix()  # абсолютный Unix-путь

        # Генерация тега
        img_tag = f'<img src="{img_path_str}" width="{size}" height="{size}"/>'

        new_text += text[last_index:start] + img_tag
        last_index = end

    new_text += text[last_index:]
    return new_text
