# pylint: disable=E0611: no-name-in-module
from pathlib import Path

import re

import emoji

EMOJI_IMAGE_DIR = Path("./00_base/source/emoji/")


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
