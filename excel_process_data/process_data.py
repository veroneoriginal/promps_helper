"""
В этом модуле реализована логика загрузки данных из таблицы
и добавление данных из json в таблицу
"""
import ast
from datetime import datetime

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
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

    def _create_dict_headers(
            self,
            sheet: Worksheet,
    ) -> dict:
        """
        Метод для создания словаря заголовков, присутствующих на листе.

        :param sheet: страница, с которой нужно взять заголовкм
        :return: словарь с заголовками и их индексамим
        """

        headers = {}
        for index, cell in enumerate(sheet[1]):
            headers[cell.value] = index
        return headers

    def write_value_to_cell(
            self,
            ws_title: str,
            row_number: int,
            column_name: str,
            value: str | int | float, ):
        """
        Записывает значение в заданную ячейку по имени столбца и номеру строки.

        :param ws_title: Название листа
        :param row_number: Номер строки (начиная с 1)
        :param column_name: Название столбца (заголовок из первой строки)
        :param value: Значение для записи
        """

        if ws_title not in self.wb.sheetnames:
            raise ValueError(f"Лист '{ws_title}' не найден в книге.")

        sheet = self.wb[ws_title]
        headers = self._create_dict_headers(sheet)

        if column_name not in headers:
            raise ValueError(f"Столбец '{column_name}' не найден среди заголовков.")

        column_index = headers[column_name] + 1
        sheet.cell(row=row_number, column=column_index, value=value)
        self.save_wb()

    def _load_data(
            self,
            ws_title: str,
            column_name: str,
    ) -> dict:
        """
        Универсальный метод для загрузки данных из Excel.

        :param ws_title: название листа
        :param column_name: название столбца, значения в ячейках
        которого будут ключами будущих словарей

        :return: словарь с загруженными данными
        """

        sheet = self.wb[ws_title]
        headers = self._create_dict_headers(sheet=sheet)

        data = {}

        # Проверяем, есть ли ключевой столбец, значения в котором будут ключами в словаре
        if column_name not in headers:
            raise ValueError(f"В листе отсутствует столбец '{column_name}'")

        # Получение индекса искомого столбца
        code_index = headers[column_name]

        # Получаем все строки, начиная со второй (после заголовков)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Получаем значение из ключевого столбца для текущей строки
            item_name = row[code_index]

            # Пропускаем строки, где название пустое
            if not item_name:
                continue

            # Создаем вложенный словарь со всеми значениями
            entry = {}
            for header, index in headers.items():
                # Пропускаем сам ключевой столбец, так как он уже ключ
                if header != column_name:
                    entry[header] = row[index]

            # Добавляем в общий словарь только если есть данные
            if entry:
                data[item_name] = entry

        return data

    def fill_row_color(
            self,
            ws_title: str,
            row_nums: tuple[int, ...],
            hex_color: str = "FF0000"
    ) -> None:
        """
        Закрашивает все строки по номерам в указанный цвет
        :param ws_title: название листа
        :param row_nums: номера строк, которые нужно покрасить (начиная с 1)
        :param hex_color: цвет в hex формате (например, "FF0000" — красный)
        """
        sheet = self.wb[ws_title]

        fill = PatternFill(fill_type="solid", fgColor=hex_color)
        for row in row_nums:
            for cell in sheet[row]:
                cell.fill = fill

    def load_info_about_products(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы Средства.xlsx -> лист "Средства",
        Из этих данных формируется словарь с учётом артикулов средств

        {
            название средства:  {
            '11111': {
                "Состав": "содержимое ячейки",
                "Тип продукта": "содержимое ячейки",
                и вся остальная информация в зависимости от кол-ва столбцов
            },
            '2222': {
                "Состав": "содержимое ячейки",
                "Тип продукта": "содержимое ячейки",
                и вся остальная информация в зависимости от кол-ва столбцов
            },
        }
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о продуктах (название является ключом)
        """

        sheet = self.wb[ws_title]
        headers = self._create_dict_headers(sheet=sheet)

        data = {}

        # Индексы нужных колонок
        product_name_idx = headers["Название"]
        product_article_idx = headers["Артикул в Золотом Яблоке"]

        # Обработка строк
        for row in sheet.iter_rows(min_row=2, values_only=True):
            name = row[product_name_idx].lower().strip()
            article = str(row[product_article_idx]).strip()

            # Создаем словарь данных по текущей строке
            entry = {}
            for header, index in headers.items():
                # Пропускаем сам ключевой столбец, так как он уже ключ
                if header and header != product_name_idx:
                    entry[header] = row[index]
                    if header == 'Элементы состава списком':
                        entry['Элементы состава списком'] = (
                            ast.literal_eval(entry['Элементы состава списком'])
                        )

            # Строим структуру
            if name not in data:
                data[name] = {}

            data[name][article] = entry

        return data

    def save_wb(
            self,
            file_path: str = None,
    ) -> None:
        """
        Метод для сохранения информации по нужному пути

        :param file_path: путь файла, в который нужно сохранять информацию
        :return: None
        """
        if file_path is None:
            self.wb.save(self.file_path)
        else:
            self.wb.save(file_path)

    def close_wb(self) -> None:
        """
        Метод для для закрытия книги эксель

        :return: None
        """
        self.wb.close()

    def load_type_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы 00_Средства -> лист "Тип"
        Из этих данных формируется словарь вида
        {
            Код: {
            'Область применения': 'содержимое ячейки',
            'Суть': 'содержимое ячейки',
            'Описание': 'содержимое ячейки',
            и т.д.
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о типах (части тела) и их характеристики
        """

        return self._load_data(ws_title=ws_title, column_name='Код')

    def load_user_request(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы 00_Средства -> лист "Запрос"
        Из этих данных формируется словарь вида
        {
           ЗВ1: {
            'Область применения': 'содержимое ячейки',
            'Суть': 'содержимое ячейки',
            и т.д.
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией запросах и их характеристиках
        """

        return self._load_data(ws_title=ws_title, column_name="Код")

    def load_tasks_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы 00_Средства -> лист "Задача"
        Из этих данных формируется словарь вида
        {
            Код: {
            'Суть': 'содержимое ячейки',
            'Описание': 'содержимое ячейки',
            и т.д.
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о задачах, которые пользователь хочет решить
        и их характеристиках
        """

        return self._load_data(ws_title=ws_title, column_name="Код")

    def load_specialists_data(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы 00_Средства -> лист "Специалист"
        Из этих данных формируется словарь вида
        {
            Код: {
            'Суть': 'Очищение у корней, баланс увлажнения',
            'Описание': 'содержимое ячейки',
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о специлисте и его описание
        """

        return self._load_data(ws_title=ws_title, column_name="Код")

    def get_column_values(
            self,
            column_title: str,
            ws_title: str,
            skip_empty: bool = False,
    ) -> dict[str | float | datetime | None, int]:
        """
        Возвращает словарь {значение_ячейки: номер_строки} из указанного столбца.
        :param column_title: название столбца (из первой строки)
        :param ws_title: название листа
        :param skip_empty: если True — пропускает пустые значения
        """
        sheet = self.wb[ws_title]

        # Получаем заголовки из первой строки
        headers = self._create_dict_headers(sheet=sheet)
        col_index = headers[column_title]

        result = {}

        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            cell_value = row[col_index]
            if skip_empty and (cell_value is None or str(cell_value).strip() == ""):
                continue
            result[cell_value] = row_num

        return result

    def get_rows_with_value_in_cell(
            self,
            target_column_title: str,
            target_column_value: str | None,
            ws_title: str,
    ) -> dict:
        """
        Возвращает все строки, у которых в определённом столбце стоит
        определённое значение.
        Возвращает словарь вида: номер строки: (кортеж значений строки)
        :param ws_title: лист, с которого берем информацию
        :param target_column_title: название целевого столбца
        :param target_column_value: значение, которое должно быть в столбце
        """
        sheet = self.wb[ws_title]

        collections = {}

        # Получаем заголовки из первой строки
        headers = self._create_dict_headers(sheet=sheet)
        target_col_index = headers.get(target_column_title)

        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            cell_value = row[target_col_index]

            if target_column_value == "":
                if cell_value is None or str(cell_value).strip() == "":
                    collections[row_num] = row
            else:
                if str(cell_value).strip().lower() == target_column_value.lower():
                    collections[row_num] = row

        return collections

    def load_info_about_collection(
            self,
            ws_title: str,
            row: tuple,
    ) -> dict:
        """
        Метод, в котором осуществляется загрузка данных из таблицы Подборки
        -> лист "Подборки" с конкретной строки и формирование из этих данных словаря вида.
        То есть добавляем заголовки столбцов к данным для удобства.
        {
        'Пол': 'женский',
        'Возраст': 30,
        'Тип': '2, 4',
        'Запрос': 2,
        'Задача': 1,
        и так далее по всем столбцам
        }

        :param ws_title: имя листа
        :param row: кортеж с значениями из строки

        :return: словарь с информацией о подборке
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headers(sheet=sheet)

        # Формируем словарь со всеми столбцами
        data = {}
        for header, index in headers.items():
            # Добавляем все значения, даже пустые
            data[header] = row[index]

        return data
