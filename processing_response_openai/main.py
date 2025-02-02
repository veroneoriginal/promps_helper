"""В этом модуле разбираем ответ от OpanAI и записываем в таблицу"""

import json
from typing import (
    Optional,
    Any,
)
import openpyxl


def checking_file_with_response(
        file_path: str,
) -> Optional[Any] | None:
    """ С помощью этой функции открываю файл с ответом OpenAI
    и проверяю, что формат файла с ответом соответствует заданному

    :param file_path: путь до файла с ответом OpenAI
    :return: JSON-данные или None
    """

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            print("✅ JSON корректный! Файл открыт.")
            return data

        except json.JSONDecodeError as e:
            print(f"❌ Ошибка в JSON: {e}")
            return None


def writing_data_from_json_to_excel(
        data: Optional[Any],
        excel_file: str,
) -> None:
    """ Функция для записи данных из json-файла с ответом OpenAI
    в Excel в "Подборки".

    :param data: JSON-данные
    :param excel_file: путь до таблицы с листом "Подборки"
    :return: None
    """

    # Загружаем существующий Excel-файл
    wb = openpyxl.load_workbook(excel_file)
    ws = wb["Подборки"]

    # Считываем заголовки и определяем их позиции
    headers = {cell.value: cell.column for cell in ws[1] if cell.value}

    # Определяем нужные столбцы
    col_best_product = headers["Лучшее средство"]
    col_recommendation = headers["Итоговая рекомендация"]

    # Определяем столбцы для рейтинга (ищем только "Средство 1", остальное идёт подряд)
    rating_columns = [headers[f"Средство {i}"] for i in range(1, 7)]

    # Ищем первую пустую строку в колонке "Лучшее средство"
    empty_row = ws.max_row + 1  # По умолчанию добавляем в конец

    for row in range(2, ws.max_row + 2):
        if ws.cell(row=row, column=col_best_product).value is None:
            empty_row = row
            break

    # Заполняем "Лучшее средство"
    ws.cell(row=empty_row, column=col_best_product, value=data["лучшее средство"])

    # Заполняем рейтинг
    for i, item in enumerate(data["рейтинг_средств"]):
        # Столбец для названия средства
        col_name = rating_columns[i]

        # Следующий столбец для плюсов
        col_pluses = col_name + 1

        # Через один столбец для минусов
        col_minuses = col_name + 2

        ws.cell(row=empty_row, column=col_name, value=item["название"])
        ws.cell(row=empty_row, column=col_pluses, value="\n".join(item["плюсы"]))
        ws.cell(row=empty_row, column=col_minuses, value="\n".join(item["минусы"]))

    # Заполняем "Итоговую рекомендацию"
    ws.cell(row=empty_row, column=col_recommendation, value=data["итоговая_рекомендация"])

    # Сохраняем изменения
    wb.save(excel_file)

    print(f"Файл успешно обновлен: {excel_file}")


def main(
        file_path: str,
        excel_file: str,
) -> None:
    """
    Функция для вызова ключевых функций модуля

    :param excel_file: путь до таблицы с листом "Подборки"
    :param file_path: путь до файла с ответом OpenAI
    :return: None
    """

    data = checking_file_with_response(file_path=file_path)
    writing_data_from_json_to_excel(
        data=data,
        excel_file=excel_file,
    )
