import json
import re
from typing import Callable
import os
import ast

from dotenv import load_dotenv
from openai import OpenAI

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

# Настройки
load_dotenv()
API_KEY = os.getenv('OPENAI_API_TECHNICAL_KEY')
MODEL = os.getenv('OPENAI_MODEL')

# Список допустимых аббревиатур, которые должны быть UPPERCASE
KNOWN_ABBREVIATIONS = {"PEG", "CI", "BHT", "EDTA", "VP", "PPG", "SLES", "SLS", "PPB", "PCA"}


def parse_list_from_string(s: str) -> list:
    """ Превратить строку в Python-список """

    return ast.literal_eval(s)


def list_to_parsable_string(ingredients: list) -> str:
    """ Превратить список обратно в строку """
    return json.dumps(ingredients, ensure_ascii=False)


def normalize_ingredient_name(text: str) -> str:
    """
    Обрабатываем регистр в названии элемента
    """
    text = text.strip()

    # Удаляем лишние пробелы
    text = re.sub(r"\s+", " ", text)

    # Обработка скобок
    def fix_substring(s):
        if s.upper() in KNOWN_ABBREVIATIONS:
            return s.upper()
        return s[:1].upper() + s[1:].lower()

    def process_segment(segment):
        # Примеры: PEG-10 Dimethicone, Sodium PCA, etc.
        words = segment.split()
        return " ".join([
            "-".join([fix_substring(part) for part in word.split("-")])
            for word in words
        ])

    # Обработка скобок вручную
    def fix_parentheses(match):
        inner = match.group(1)
        return "(" + process_segment(inner) + ")"

    text = re.sub(r"\(([^)]+)\)", fix_parentheses, text)

    return process_segment(text)


def fix_ingredient_string(elements: list) -> list:
    """
    Цикл обработки имён элементов
    """
    return [normalize_ingredient_name(element) for element in elements]


def get_filtered_elements(composition_text: str) -> tuple:
    """
    Отправляет запрос.
    Исправляет регистр букв
    Возвращает готовую строку после запроса
    """

    content = ask_openai_about_composition(composition_text=composition_text)
    _list = parse_list_from_string(content)
    count_list = len(_list)
    capitalize_str = fix_ingredient_string(_list)
    return list_to_parsable_string(capitalize_str), count_list


def ask_openai_about_composition(composition_text: str) -> str:
    """
    Отправляет состав в OpenAI и просит разбить его на список.
    Возвращает результат в виде строки.
    """
    client = OpenAI(api_key=API_KEY)

    messages = [
        {
            "role": "system",
            "content": "Не пиши ничего лишнего, пиши только названия элементов. "
                       "Если есть какие-то пояснения - убирай их."
        },
        {
            "role": "user",
            "content": f"Вот состав:\n{composition_text}\n\nВерни только "
                       f"список элементов состава в виде строки, в которой каждый "
                       f"элемент в кавычках."
                       f"В начале строки стоит [ и в конце стоит ]."
                       f"Если элемент один, например, 'Сульфат магния', значит "
                       f"делаешь список из одного элемента, но не раскладываешь "
                       f"элемент на несколько."
                       f"Не нужно писать никаких описаний, пояснений к элементам и прочего, "
                       f"только их названия."
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content.strip()


def get_rows_for_check_composition(
        ws: Worksheet,
        source_column_name: str,
        target_column_name: str,
        target_len_column_name: str,
):
    """
    Получаем все строки для обработки составов
    """
    headers = [cell.value for cell in ws[1]]
    col_index = {
        source_column_name: headers.index(source_column_name) + 1,
        target_column_name: headers.index(target_column_name) + 1,
        target_len_column_name: headers.index(target_len_column_name) + 1,
    }

    rows_to_process = []
    for row in ws.iter_rows(min_row=2):
        source_cell = row[col_index[source_column_name] - 1]
        target_cell = row[col_index[target_column_name] - 1]
        target_len_cell = row[col_index[target_len_column_name] - 1]

        if not target_cell.value and source_cell.value:
            rows_to_process.append(
                (source_cell.value, target_cell, target_len_cell, source_cell.row)
            )
    total = len(rows_to_process)
    if total:
        print(f"🔍 Найдено строк для обработки: {total}")
    else:
        print('⚠️ Нет пустых составов для обработки')
    return rows_to_process


# pylint: disable=R0913: too-many-arguments
# pylint: disable=R0917: too-many-positional-arguments
# pylint: disable=R0914: too-many-locals
def process_excel_and_fill_composition(
        file_path_tools: str,
        sheet_name: str,
        source_column_name: str,
        target_column_name: str,
        target_len_column_name: str,
        progress_callback: Callable | None = None,

):
    """
    Обрабатывает составы средств.
    Записывает в столбец "Элементы состава списков" строку, готовую к
    превращению в Python-список
    :param file_path_tools: путь до таблицы со всей инфой о средствах, типах и прочем
    :param sheet_name: название листа
    :param source_column_name: название столбца с "сырым" текстом состава
    :param target_column_name: название столбца, куда записывать обработанный состав
    :param target_len_column_name: название столбца, куда записывать количество элементов состава
    :param progress_callback: коллбэк для обновления прогресс бара

    """
    wb = openpyxl.load_workbook(file_path_tools)
    ws = wb[sheet_name]

    # 1. Собираем все строки, которые надо обработать
    rows_to_process = get_rows_for_check_composition(
        ws=ws,
        source_column_name=source_column_name,
        target_column_name=target_column_name,
        target_len_column_name=target_len_column_name,
    )
    total = len(rows_to_process)

    # 2. Обрабатываем
    for index, (
            composition,
            target_cell,
            target_len_cell,
            row_number
    ) in enumerate(rows_to_process, start=1):
        print(f" Обрабатываем: {composition[:40]}...")
        try:
            parsed, count = get_filtered_elements(composition)
            if parsed:
                target_cell.value = parsed
                target_len_cell.value = count
                print(f"✅ Записано элементов состава: {count}")
            else:
                wb.save(file_path_tools)
                print("⚠️ Не удалось обработать элементы состава.")
                return
        except Exception as exc:
            wb.save(file_path_tools)
            print(f"❌ Ошибка в строке № {row_number}: {exc}")
            raise

        if progress_callback:
            progress_callback(index, total)

    wb.save(file_path_tools)
    print("💾 Готово! Всё сохранено.")
