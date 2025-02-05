from typing import Optional
import datetime

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
