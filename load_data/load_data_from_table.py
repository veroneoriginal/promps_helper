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

    def load_hair_type_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Типы волос"
        Из этих данных формируется словарь вида
        {
            1: {
            'Тип': 'Сухие волосы',
            'Описание': 'содержимое ячейки',
            'Хештег': 'содержимое ячейки',
            },

            2: {
            'Тип': 'Нормальные волосы',
            'Описание': 'содержимое ячейки',
            'Хештег': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о типе волос и их характеристике
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headings(sheet=sheet)

        hair_type_data = {}

        # Проходим по строкам, начиная со второй (первая - заголовки)
        for row in sheet.iter_rows(min_row=2, values_only=True):

            key = row[headers["№"]]
            hair_type = row[headers["Тип"]]
            description = row[headers["Описание"]]
            hashtag = row[headers["Хештег"]]

            if all([hair_type, description, hashtag]):
                hair_type_data[int(key)] = {
                    "Тип": hair_type,
                    "Описание": description,
                    "Тег": hashtag,
                }

        return hair_type_data

    def load_head_skin_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Типы кожи головы"
        Из этих данных формируется словарь вида
        {
            1: {
            'Тип': 'Нормальная кожа головы',
            'Описание': 'содержимое ячейки',
            },

            2: {
            'Тип': 'Сухая кожа головы',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о типах кожи головы и их характеристике
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headings(sheet=sheet)

        head_skin_type_data = {}

        # Проходим по строкам, начиная со второй (первая - заголовки)
        for row in sheet.iter_rows(min_row=2, values_only=True):

            key = row[headers["№"]]
            head_skin_type = row[headers["Тип"]]
            description = row[headers["Описание"]]

            if all([head_skin_type, description]):
                head_skin_type_data[int(key)] = {
                    "Тип": head_skin_type,
                    "Описание": description,
                }

        return head_skin_type_data

    def load_problems_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Загрузка данных из таблицы 00_Средства -> лист "Проблемы"
        Из этих данных формируется словарь вида
        {
            1: {
            'Проблема': 'Восстановление поврежденной структуры',
            'Описание': 'содержимое ячейки',
            },

            2: {
            'Проблема': 'Выпадение волос',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о проблемах и их характеристиках
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headings(sheet=sheet)

        problems_data = {}

        # Проходим по строкам, начиная со второй (первая - заголовки)
        for row in sheet.iter_rows(min_row=2, values_only=True):

            key = row[headers["№"]]
            problem = row[headers["Проблема"]]
            description = row[headers["Описание"]]

            if all([problem, description]):
                problems_data[int(key)] = {
                    "Проблема": problem,
                    "Описание": description,
                }

        return problems_data

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

            2: {
            'Потребность': 'Интенсивное увлажнение и питание кончиков',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о потребностях клиента и их детальном описании
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headings(sheet=sheet)

        wishes_data = {}

        # Проходим по строкам, начиная со второй (первая - заголовки)
        for row in sheet.iter_rows(min_row=2, values_only=True):

            key = row[headers["№"]]
            wish = row[headers["Потребность"]]
            description = row[headers["Описание"]]

            if all([wish, description]):
                wishes_data[int(key)] = {
                    "Потребность": wish,
                    "Описание": description,
                }

        return wishes_data

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
                    "Пожелания": row[headers["Пожелания"]],
                }

        # Если не нашли пустую строку - значит новых данных о пользователе нет
        return {}
