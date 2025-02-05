"""
В этом модуле реализована логика загрузки данных из таблицы
и добавление данных из json в таблицу
"""
import sys
from typing import (
    Optional,
    Any,
)

import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from excel_process_data.utils.utils import find_empty_row_for_today


class ExcelManager:
    """
    Класс для работы с Excel-файлом

    :param file_path: путь до обрабатываемого документа
    :return: None
    """

    def __init__(
            self,
            file_path: str,
    ):
        self.file_path = file_path
        self.wb = load_workbook(self.file_path)

    def _create_dict_headers(
            self,
            sheet: Worksheet,
    ) -> dict:
        """
        В этой функции создается словарь заголовков, присутствующих на листе

        :param sheet: страница, с которой нужно взять заголовкм
        :return: словарь с заголовками и их индексамим
        """

        headers = {}
        for index, cell in enumerate(sheet[1]):
            headers[cell.value] = index

        return headers

    def _load_data(
            self,
            ws_title: str,
            fields: tuple,
            filter_column: str = None,
            filter_value: str = None,
    ) -> dict:
        """
        Универсальный метод для загрузки данных из Excel.

        :param ws_title: название листа
        :param fields: список заголовков Excel, которые нужно загрузить
        :param filter_column: название столбца, по кот. нужно фильтровать данные (опционально)
        :param filter_value: значение-фильтр (опционально)
        :return: словарь с загруженными данными
        """
        sheet = self.wb[ws_title]
        headers = self._create_dict_headers(sheet=sheet)
        data = {}

        # Определение индекса столбца для фильтрации (если указано)
        filter_index = headers.get(filter_column) if filter_column else None

        item_id = 1
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Если указан фильтр, проверяем значение в соответствующем столбце
            if filter_index is not None and row[filter_index] != filter_value:
                continue  # Пропускаем строки, которые не соответствуют фильтру

            # Создаём пустой словарь
            entry = {}

            for key in fields:
                entry[key] = row[headers[key]]

            if all(entry.values()):
                data[item_id] = entry
                item_id += 1

        return data

    def _save_wb(
            self,
            file_path: str = None,
    ) -> None:
        """
        Функция для сохранения информации по нужному пути

        :param file_path: путь файла, в который нужно сохранять информацию
        :return: None
        """
        if file_path is None:
            self.wb.save(self.file_path)
        else:
            self.wb.save(file_path)

    def load_hair_type_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Типы волос"
        Из этих данных формируется словарь вида
        {
            1: {
            'Тип': 'содержимое ячейки',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о типе волос и их характеристике
        """

        return self._load_data(
            ws_title=ws_title,
            fields=("Тип", "Описание"),
        )

    def load_head_skin_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Типы кожи головы"
        Из этих данных формируется словарь вида
        {
            1: {
            'Тип': 'содержимое ячейки',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о типах кожи головы и их характеристике
        """

        return self._load_data(
            ws_title=ws_title,
            fields=("Тип", "Описание"),
        )

    def load_problems_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Проблемы"
        Из этих данных формируется словарь вида
        {
            1: {
            'Проблема': 'содержимое ячейки',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о проблемах и их характеристиках
        """

        return self._load_data(
            ws_title=ws_title,
            fields=("Проблемы", "Описание"),
        )

    def load_wishes_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Потребности"
        Из этих данных формируется словарь вида
        {
            1: {
            'Потребность': 'Очищение у корней, баланс увлажнения',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о потребностях клиента и их детальном описании
        """

        return self._load_data(
            ws_title=ws_title,
            fields=("Потребности", "Описание"),
        )

    def load_info_about_user(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Подборки"

        Из этих данных формируется словарь вида
        {
        'Пол': 'женский',
        'Возраст': 30,
        'Тип волос': '2, 4',
        'Тип кожи головы': 1,
        'Проблемы': 2,
        'Потребности': 1,
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о пользователе или пустой словарь,
        если новых данных о пользователе нет

        """
        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headers(sheet=sheet)

        # Поиск первой строки, где ячейка в столбце "Лучшее средство" пустая
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Если ячейка "Лучшее средство" пустая
            if not row[headers["Лучшее средство"]]:
                return {
                    "Пол": row[headers["Пол"]],
                    "Возраст": row[headers["Возраст"]],
                    "Тип волос": row[headers["Тип волос"]],
                    "Тип кожи головы": row[headers["Тип кожи головы"]],
                    "Проблемы": row[headers["Проблемы"]],
                    "Потребности": row[headers["Потребности"]],
                }

        # Если не нашли пустую строку - значит новых данных о пользователе нет
        return {}

    def load_info_about_products(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Средства",
        учитывая только строки, где 'Новое' == 'да'.
        Из этих данных формируется словарь вида

        {
            1: {
                "Название": "содержимое ячейки",
                "Состав": "содержимое ячейки",
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о продуктах (название и состав)
        """

        return self._load_data(
            ws_title=ws_title,
            fields=("Название", "Состав"),
            filter_column="Новое",
            filter_value="да")

    def write_products(
            self,
            ws: Worksheet,
            data: Optional[Any],
            empty_row: int,
            headers: dict,
    ) -> None:

        """
        Функция осуществляет запись о средствах из Json-файла в лист Подборки

        :param ws: активный лист из excel-документа
        :param data: JSON - данные
        :param empty_row: номер строки, в которую будет осуществляться запись
        :param headers: словарь сназваниями столбцов и их номерами

        :return: None
        """

        # Определяем названия столбцов по заголовкам, например "Средство 1", "Средство 2" и т.д.
        rating_columns = []
        i = 1
        while f"Средство {i}" in headers:
            rating_columns.append(headers[f"Средство {i}"])
            i += 1

        product_index = 1
        rating_index = 0
        while True:
            product_key = f"product_{product_index}"
            if product_key not in data:
                break
            product_data = data[product_key]
            if rating_index < len(rating_columns):
                col_name = rating_columns[rating_index]
                col_pluses = col_name + 1  # предполагаем, что плюсы в следующем столбце
                col_minuses = col_name + 2  # а минусы — через один после плюсов

                ws.cell(row=empty_row, column=col_name, value=product_data["title"])
                ws.cell(row=empty_row, column=col_pluses, value=product_data["plus"])
                ws.cell(row=empty_row, column=col_minuses, value=product_data["minus"])
            else:
                print(f"Предупреждение: для {product_key} "
                      f"не найдены соответствующие столбцы в Excel.")
            product_index += 1
            rating_index += 1

    def writing_data_from_json_to_excel(
            self,
            data: Optional[Any],
    ) -> None:
        """ Функция для записи данных из json-файла с ответом OpenAI
        в Excel в лист "Подборки".

        :param data: JSON-данные
        :return: None
        """

        if data is None:
            print("⛔ Ошибка: JSON-файл пустой или некорректный. Останавливаю выполнение.")
            sys.exit()

        # Загружаем существующий Excel-файл
        ws = self.wb["Подборки"]

        # Считываем заголовки и определяем их позиции
        headers = {cell.value: cell.column for cell in ws[1] if cell.value}

        # Определяем нужные столбцы
        col_best_product = headers["Лучшее средство"]
        col_recommendation = headers["Итоговая рекомендация"]
        col_date = headers["Дата"]

        # Определяем текущую дату в нужном формате (например, "ДД.ММ.ГГГГ")
        today_str = datetime.date.today().strftime("%d.%m.%Y")

        # Ищем строку с текущей датой и пустой ячейкой в столбце "Лучшее средство"
        empty_row = find_empty_row_for_today(
            ws=ws,
            col_date=col_date,
            col_best_product=col_best_product,
            today_str=today_str,
        )
        if empty_row is None:
            print(f"⛔ Ошибка: для даты {today_str} не найдена пустая строка для записи.")
            sys.exit()

        # Запись лучшего средства в таблицу из json-файла
        ws.cell(row=empty_row, column=col_best_product, value=data["best_product"])

        # Запись данных по продуктам
        self.write_products(ws, data, empty_row, headers)

        # Блок 5: Запись итоговой рекомендации
        ws.cell(row=empty_row, column=col_recommendation, value=data["result"])

        # Сохраняем изменения
        self._save_wb()

        print(f"Лист 'Подборки' успешно обновлен: {self.file_path}")
