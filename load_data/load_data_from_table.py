""" В этом модуле реализована логика загрузки данных из таблицы """

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelManager:

    def __init__(self, file_path):
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
        "1": {
            "Нормальные волосы": (
                                "содержимое ячейки с описанием",
                                "содержимое ячейки с хештегом",
             )
        },

        "2": {
            "Сухие волосы": (
                            "содержимое ячейки с описанием",
                            "содержимое ячейки с хештегом",
             )
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

            key = str(row[headers["№"]])
            hair_type = row[headers["Тип"]]
            description = row[headers["Описание"]]
            hashtag = row[headers["Хештег"]]

            if hair_type and description and hashtag:
                hair_type_data[key] = {hair_type: (description, hashtag)}

        return hair_type_data
