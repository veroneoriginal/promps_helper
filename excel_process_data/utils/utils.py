import re
import datetime
from typing import Optional
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


def find_empty_row_for_today(
        ws: Worksheet,
        col_date: int,
        col_best_product: int,
        today_str: str,
) -> Optional[int] | None:
    """
    Функция определяет строку для вставки средств по текущей дате
    и свободной ячейке в столбце "Лучшее средство"

    :param ws: активный лист из excel-документа
    :param col_date: номер столбца "Дата"
    :param col_best_product: номер столбца "Лучший продукт"
    :param today_str: текущая дата

    :return: номер строки, в которую будет осуществляться запись
    """

    for row in range(2, ws.max_row + 1):
        cell_value = ws.cell(row=row, column=col_date).value
        if isinstance(cell_value, datetime.date):
            cell_date_str = cell_value.strftime("%d.%m.%Y")
        elif cell_value is not None:
            cell_date_str = str(cell_value)
        else:
            cell_date_str = ""

        if cell_date_str == today_str:
            # Нашли строку с нужной датой, теперь проверяем, пуста ли ячейка "Лучшее средство"
            if ws.cell(row=row, column=col_best_product).value is None:
                return row
    # если пустой строки для текущей даты не найдено
    return None


def find_target_row_for_today_and_full_best_product(
        sheet: Worksheet,
        today_data: str,
        headers: dict,
) -> Optional[int] | None:
    """
    Функция определяет строку для вставки средств по текущей дате
    и свободной ячейке в столбце "Лучшее средство"

    :param sheet: активный лист из excel-документа
    :param headers: словарь с заголовками и нумерацией
    :param today_data: текущая дата

    :return: номер строки, в которую будет осуществляться запись
    """

    for row in range(2, sheet.max_row + 1):
        date_cell = sheet.cell(row=row, column=headers["Дата"]).value
        best_product = sheet.cell(row=row, column=headers["Лучшее средство"]).value

        if date_cell and best_product:
            if isinstance(date_cell, datetime.datetime):
                date_cell = date_cell.strftime("%d.%m.%Y")

            if date_cell == today_data:
                return row

    raise ValueError("Нет строки с сегодняшней датой и заполненным 'Лучшее средство'.")


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
            "плюсы": plus,
            "минусы": minus,
            "лучшее средство": (name == best_mean)
        }

    return selection_dict


def creating_dict_for_pdf(
        dict_full_info: dict,
) -> dict:
    """
    Функция для сбора данных (словаря), необходимых для вставки в pdf.
    Словарь имеет вид
    {
    Название : описание,
    Плюсы : описание,
    Минусы : описание,
    Количество меры (число) : описание,
    Юниты меры (мл/шт): описание,
    Стоимость руб: описание,
    Ссылка на изображение в базе: описание,
    }
    """

    dict_for_picture = {}

    # Дополнительные ключи, которые мы нужно взять из полного словаря
    additional_keys = [
        "Количество меры (число)",
        "Юниты меры (мл/шт)",
        "Стоимость руб",
        "Ссылка на изображение в базе",
    ]

    for product_name, info in dict_full_info.items():

        # Пропускаем ключ, если он не относится к конкретному средству
        if product_name == "итоговая рекомендация":
            continue

        # Формирование нового словаря для средства с нужными ключами
        new_info = {
            "Название": product_name,
            "Плюсы": info.get("плюсы"),
            "Минусы": info.get("минусы")
        }
        # Добавляем дополнительные данные
        for key in additional_keys:
            new_info[key] = info.get(key, "")

        dict_for_picture[product_name] = new_info

    return dict_for_picture
