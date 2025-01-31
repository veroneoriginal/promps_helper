""" В этом модуле реализована логика загрузки данных из таблицы """

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


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

    def _create_dict_headings(
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
            mapping: dict,
            filter_column: str = None,
            filter_value: str = None,
    ) -> dict:
        """
        Универсальный метод для загрузки данных из Excel.

        :param ws_title: название листа
        :param mapping: соответствие между заголовками в Excel и ключами в выходном словаре
        :param filter_column: название столбца, по кот. нужно фильтровать данные (опционально)
        :param filter_value: значение-фильтр (опционально)
        :return: словарь с загруженными данными
        """
        sheet = self.wb[ws_title]
        headers = self._create_dict_headings(sheet=sheet)
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

            # Проходим по соответствию ключей
            for excel_key, output_key in mapping.items():
                value = row[headers[excel_key]]
                entry[output_key] = value

            if all(entry.values()):
                data[item_id] = entry
                item_id += 1

        return data

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

        mapping = {
            "Тип": "Тип",
            "Описание": "Описание",
        }

        return self._load_data(ws_title, mapping)

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

        mapping = {
            "Тип": "Тип",
            "Описание": "Описание",
        }

        return self._load_data(ws_title, mapping)

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

        mapping = {
            "Проблема": "Проблема",
            "Описание": "Описание",
        }

        return self._load_data(ws_title, mapping)

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

        mapping = {
            "Потребность": "Потребность",
            "Описание": "Описание",
        }

        return self._load_data(ws_title, mapping)

    def load_info_about_user(
            self,
            ws_title: str,
    ) -> dict | None:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Подборки"

        Из этих данных формируется словарь вида
        {
        'Пол': 'женский',
        'Возраст': 30,
        'Тип волос': '2, 4',
        'Тип кожи головы': 1,
        'Проблема': 2,
        'Пожелания': 1,
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о пользователе или пустой словарь,
        если новых данных о пользователе нет

        """
        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headings(sheet=sheet)

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
                    "Потребности": row[headers["Пожелания"]],
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

        mapping = {
            "Название": "Название",
            "Состав": "Состав",
        }

        return self._load_data(
                ws_title,
                mapping,
                filter_column="Новое",
                filter_value="да")
