""" В этом модуле реализована логика загрузки данных из таблицы """

from openpyxl import load_workbook


def _load_info_about_user(
        file_path: str,
        ws_title: str,
) -> dict | None:
    """
    Загрузка данных из таблицы 00_Средства -> лист "Подборки"
    Из этих данных формируется словарь вида
    {
     "Пол": "содержимое ячейки",
     "Возраст": "содержимое ячейки",
     "Тип волос": "содержимое ячейки",
     "Тип кожи головы": "содержимое ячейки",
     "Особенности": "содержимое ячейки",
     "Проблемы или пожелания": "содержимое ячейки",
    }

    :param file_path: путь до документа xlsx
    :param ws_title: название листа, с которого забирать информацию
    :return: словарь с информацией о пользователе или пустой словарь,
    если новых данных о пользователе нет

    """
    # Открытие файла Excel
    workbook = load_workbook(file_path)
    sheet = workbook[ws_title]

    # Создание словаря заголовков через цикл
    headers = {}
    for index, cell in enumerate(sheet[1]):
        headers[cell.value] = index

    # Поиск первой строки, где ячейка в столбце "Лучшее средство" пустая
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Если ячейка "Лучшее средство" пустая
        if not row[headers["Лучшее средство"]]:
            return {
                "Пол": row[headers["Пол"]],
                "Возраст": row[headers["Возраст"]],
                "Тип волос": row[headers["Тип волос"]],
                "Тип кожи головы": row[headers["Тип кожи головы"]],
                "Проблема": row[headers["Проблема"]],
                "Пожелания": row[headers["Пожелания"]],
            }

    workbook.close()

    # Если не нашли пустую строку - значит новых данных о пользователе нет
    return {}


def _load_info_about_products(
        file_path: str,
        ws_title: str,
) -> dict:
    """
    Загрузка данных из таблицы 00_Средства -> лист "Средства"
    Из этих данных формируется словарь вида

    {
        1: {
            "Название": "содержимое ячейки",
            "Состав": "содержимое ячейки",
        },
        2: {
            "Название": "содержимое ячейки",
            "Состав": "содержимое ячейки",
        },
        3: {
            "Название": "содержимое ячейки",
            "Состав": "содержимое ячейки",
        }
    }

    :param file_path: путь до документа xlsx
    :param ws_title: название листа, с которого забирать информацию
    :return: словарь с информацией о продуктах (название и состав)
    """
    # Загрузка файла Excel
    workbook = load_workbook(file_path)

    # Открытие листа "Средства"
    sheet = workbook[ws_title]

    # Определение индексов ключевых столбцов
    headers = {}
    for col_index, cell in enumerate(sheet[1]):
        headers[cell.value] = col_index

    # Индексы столбцов
    index_filled = headers["Заполнено"]
    index_name = headers["Название"]
    index_composition = headers["Состав"]

    # Словарь для сохранения данных
    products_info = {"Средства": {}}

    # Начальный идентификатор
    product_id = 1

    # Проходим по строкам начиная со второй (первая строка — заголовки)
    for row_index, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        filled_value = row[index_filled].value
        # Если "Заполнено" = "да"
        if filled_value == "да":
            # Сохраняем данные в словарь
            products_info["Средства"][product_id] = {
                "Название": row[index_name].value,
                "Состав": row[index_composition].value,
            }
            product_id += 1

            # Обновляем ячейку "Заполнено" на "проанализировано"
            sheet.cell(row=row_index, column=index_filled + 1, value="проанализировано")

    # Сохраняем изменения в Excel
    workbook.save(file_path)
    workbook.close()

    return products_info
