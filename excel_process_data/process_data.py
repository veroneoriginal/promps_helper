"""
В этом модуле реализована логика загрузки данных из таблицы
и добавление данных из json в таблицу
"""

import sys
import ast

from typing import (
    Optional,
    Any,
)

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from excel_process_data.utils.utils import counting_hash


# from excel_process_data.utils.utils import (
#     find_target_row_for_today_and_full_best_product,
#     find_amount_funds,
#     function_for_forming_dict_with_correlation,
# )


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

    def _create_headers_numerate(
            self,
            sheet: Worksheet,
    ) -> dict:
        """
        Создаёт словарь заголовков из первой строки указанного листа Excel.
        Функция проходит по первой строке листа Excel и формирует словарь,
        где ключами являются значения заголовков (названия столбцов),
        а значениями — их порядковые номера (начиная с 1, как в openpyxl).

        Это удобно для быстрого поиска нужного столбца по названию заголовка.

        :param sheet: Объект Worksheet (лист из Excel-файла), откуда берутся заголовки.
        :return: Словарь { "Название столбца": индекс_столбца }, где индекс начинается с 1.
        """

        return {cell.value: idx + 1 for idx, cell in enumerate(sheet[1])}

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

    def load_info_about_products(
            self,
            ws_title: str,
    ) -> dict:
        """
        Метод для загрузки данных из таблицы Средства.xlsx -> лист "Средства",
        Из этих данных формируется словарь вида

        {
            название средства: {
                "Состав": "содержимое ячейки",
                "Тип продукта": "содержимое ячейки",
                и вся остальная информация в зависимости от кол-ва столбцов
            },
        }

        :param ws_title: название листа, с которого забирать информацию
        :return: словарь с информацией о продуктах (название является ключом)
        """

        return self._load_data(ws_title=ws_title, column_name='Название')

    def _save_wb(
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

    def count_empty_result(
            self,
            ws_title: str = "Подборки",
    ) -> int:
        """
        Метод для подсчитывания количества строк в таблице 'Подборки' с незаполненным полем 'Итог'.

        :param ws_title: название листа (по умолчанию "Подборки")
        :return: количество строк с пустым полем 'Итог'
        """
        sheet = self.wb[ws_title]
        headers = self._create_dict_headers(sheet=sheet)

        # Проверяем, есть ли столбец "Итог"
        if "Итог" not in headers:
            raise ValueError("В листе отсутствует столбец 'Итог'")

        # Индекс столбца "Итог"
        result_index = headers["Итог"]

        # Счетчик пустых значений
        empty_count = 0

        # Проходим по всем строкам, начиная со второй
        for row in sheet.iter_rows(min_row=2, values_only=True):
            result_value = row[result_index]
            # Считаем пустые или None значения
            if not result_value:
                empty_count += 1

        return empty_count

    def get_data_from_table_in_form_of_dict(
            self,
            ws_title: str,
            checking_unique: bool,
    ) -> dict:
        """
        Метод, в котором:
        1) получаем данные из таблицы и преобразовываем их в словарь
        2) считаем хеш текущей подборки
        3) проверяем уникальность этой подборки

        :param ws_title: лист, с которого берем информацию
        :param checking_unique: параметр, который отвечает за запись или незапись хеша в таблицу
        :return: возвращает либо словарь с данными о подборке (если она уникальная),
        либо возбуждает исключение и код дальше не идет
        """

        # Открытие файла Excel на нужном листе
        sheet = self.wb[ws_title]

        # Создание словаря заголовков
        headers = self._create_dict_headers(sheet=sheet)

        # Индекс столбца "Итог"
        result_index = headers["Итог"]

        # Индекс столбца "Хеш"
        hash_column_index = headers["Хеш"]

        # Находим строку, с которой работаем
        current_row = self.find_first_empty_row(
            sheet=sheet,
            result_index=result_index,
        )

        # получаем данные из таблицы и преобразовываем их в словарь
        dict_collection = self.load_info_about_collection(
            sheet=sheet,
            number_row=current_row,
            headers=headers,
        )

        # считаем хеш текущей подборки
        hash_collection = str(counting_hash(data=dict_collection))
        dict_collection['Хеш'] = hash_collection

        # проверяем уникальность этой подборки
        self.checking_unique_current_collection(
            hash_value=hash_collection,
            hash_column_index=hash_column_index,
            sheet=sheet,
        )
        if checking_unique:
            # запись значения хеша в xlsx в строку с текущей подборкой
            sheet.cell(row=current_row, column=hash_column_index + 1, value=hash_collection)

            # Сохраняем изменения в файл
            self.wb.save(self.file_path)

        # по ключу получаем строку, которая только внешне имеет вид словаря
        products = dict_collection['Средства']

        # Заменяем нестандартных кавычек на обычные
        normalized_products = products.replace('«', '"').replace('»', '"')

        # Превращаем строку в словарь и обновляем
        dict_collection['Средства'] = ast.literal_eval(normalized_products)

        return dict_collection

    def find_first_empty_row(
            self,
            sheet: Worksheet,
            result_index: int,
    ) -> int:
        """
        Метод для поиска первой строки, где ячейка в столбце 'Итог' пустая.

        :param sheet: лист, с которого забирать информацию
        :param result_index: индекс столбца итог
        :return: возвращаем индекс нужной строки
        """
        for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            # Если row[result_index] содержит None или пустую строку
            # то not row[result_index] вернёт True
            if not row[result_index]:
                return row_index
        raise ValueError("Не найдена пустая ячейка в столбце 'Итог'")

    def load_info_about_collection(
            self,
            sheet: Worksheet,
            headers: dict,
            number_row: int,
    ) -> dict:
        """
        Метод, в котором осуществляется загрузка данных из таблицы Подборки
        -> лист "Подборки" с конкретной строки и формирование из этих данных словаря вида
        {
        'Пол': 'женский',
        'Возраст': 30,
        'Тип': '2, 4',
        'Запрос': 2,
        'Задача': 1,
        и так далее по всем столбцам
        }

        :param sheet: лист, с которого забирать информацию
        :param headers: словарь заголовков
        :param number_row: номер строки, с которой забирать информацию

        :return: словарь с информацией о подборке
        """

        row = [cell.value for cell in sheet[number_row]]

        # Формируем словарь со всеми столбцами
        data = {}
        for header, index in headers.items():
            # Добавляем все значения, даже пустые
            data[header] = row[index]

        return data

    def checking_unique_current_collection(
            self,
            hash_value: str,
            hash_column_index: int,
            sheet: Worksheet
    ) -> bool:
        """
        Метод для проверки уникальности текущей подборки.

        :param hash_value: хеш текущей подборки
        :param hash_column_index: индекс столбца, в котором брать другие хеши
        :param sheet: лист, на котором осуществляется поиск

        :return: True или выбрасывает исключение
        """

        # получаем букву столбца
        column_letter = get_column_letter(hash_column_index + 1)

        # Получаем все значения столбца
        values = [cell.value for cell in sheet[column_letter]]

        # проверяю есть ли текущий хеш во взятых значениях
        if hash_value in values:
            raise ValueError("Такая подборка уже существует.")
        return True  # то есть такой подборки еще нет

    def update_excel_with_json(
            self,
            data: Optional[Any],
            dict_with_hash: dict,
            file_path: str,
    ) -> None:
        """
        Метод для записи данных из json-файла с ответом OpenAI в
        лист "Подборки" в итог текущей подборки

        :param data: JSON-данные
        :param dict_with_hash: словарь с текущей подборкой (для получения хеша)
        :param file_path: путь до документа Подборки.xlsx
        :return: None
        """
        print('зашли в update_excel_with_json')
        print(f'{data=}')

        if data is None:
            print("⛔ Ошибка: JSON-файл пустой или некорректный. Останавливаю выполнение.")
            sys.exit()

        # Загружаем существующий Excel-файл
        ws = self.wb["Подборки"]

        # Считываем заголовки и определяем их позиции
        headers = {cell.value: cell.column for cell in ws[1] if cell.value}

        # Определяем нужные столбцы
        col_best_product = headers["Лучший вариант"]
        col_recommendation = headers["Итог"]
        col_hash = headers["Хеш"]

        # Берем хеш из словаря
        hash_value = dict_with_hash["Хеш"]

        # Перебираем строки, начиная со 2-й (1-я — заголовки)
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=False):
            cell_hash = row[col_hash - 1]  # -1, так как индексация с 0 в списке `row`

            if cell_hash.value == hash_value:
                # print('строка по хешу найдена')
                # Записываем "Лучший вариант" и "Итог" из JSON
                row[col_best_product - 1].value = data.get("best_product", "")
                row[col_recommendation - 1].value = data.get("result", "")

        # Сохраняем изменения
        self._save_wb(file_path=file_path)
