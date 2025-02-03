"""
В этом модуле реализована логика загрузки данных из таблицы
и добавление данных из json в таблицу
"""
import sys
from typing import (
    Optional,
    Any,
)

from datetime import datetime
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

        # Определяем столбцы для рейтинга (ищем только "Средство 1", остальное идёт подряд)
        rating_columns = [headers[f"Средство {i}"] for i in range(1, 7)]

        # Ищем первую пустую строку в колонке "Лучшее средство"
        empty_row = ws.max_row + 1  # По умолчанию добавляем в конец

        for row in range(2, ws.max_row + 2):
            if ws.cell(row=row, column=col_best_product).value is None:
                empty_row = row
                break

        # Заполняем "Лучшее средство"
        ws.cell(row=empty_row, column=col_best_product, value=data["Лучшее средство"])

        # Заполняем рейтинг
        for i, item in enumerate(data["Рейтинг средств"]):
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
        ws.cell(row=empty_row, column=col_recommendation, value=data["Итоговая рекомендация"])

        # Сохраняем изменения
        self._save_wb()

        print(f"Лист 'Подборки' успешно обновлен: {self.file_path}")

    # pylint: disable= R0914 too-many-locals
    def forming_dict_from_collection(
            self,
            ws_title: str,
    ) -> dict:
        """
        В этой функции осуществляется формирование словаря из листа 'Подборки'

        :param ws_title: имя листа, с которого берем информацию
        :return: словарь со средствами из подборки и итоговой рекомендацией
        """

        ws = self.wb[ws_title]

        # Определение сегодняшней даты
        today_data = datetime.today().strftime('%d.%m.%Y')

        # Поиск индексов нужных столбцов
        headers = {cell.value: idx + 1 for idx, cell in enumerate(ws[1])}

        # Поиск строки с сегодняшней датой
        target_row = None
        for row in range(2, ws.max_row + 1):
            cell_value = ws.cell(row=row, column=headers["Дата"]).value
            cell_str = cell_value.strftime("%d.%m.%Y") \
                if isinstance(cell_value, datetime) else str(cell_value)
            if cell_str == today_data:
                target_row = row
                break

        if not target_row:
            raise ValueError("Не найдена строка с сегодняшней датой.")

        # Считываем значение лучшего средства (оно должно совпадать с названием одного из средств)
        best_product_value = ws.cell(row=target_row, column=headers["Лучшее средство"]).value

        # Считываем итоговую рекомендацию
        final_rec_value = ws.cell(row=target_row, column=headers["Итоговая рекомендация"]).value

        # Формируем словарь с данными для 6 средств
        products_dict = {}
        for i in range(1, 7):
            # Считываем название, плюсы и минусы для средства i
            product_name = ws.cell(row=target_row, column=headers[f"Средство {i}"]).value
            plus = ws.cell(row=target_row, column=headers[f"Средство {i}\nПЛЮСЫ"]).value
            minus = ws.cell(row=target_row, column=headers[f"Средство {i}\nМИНУСЫ"]).value

            products_dict[product_name] = {
                "плюсы": plus,
                "минусы": minus,
                "лучшее средство": (product_name == best_product_value)
            }

        # Собираем итоговый словарь: добавляем рекомендацию
        products_dict["итоговая рекомендация"] = final_rec_value

        return products_dict

    def add_data_from_the_tools_page(
            self,
            ws_title: str,
            data: dict,
    ) -> dict:
        """Функция добавляет информацию к словарю со средствами из подборки"""

        ws = self.wb[ws_title]

        headers = {cell.value: idx + 1 for idx, cell in enumerate(ws[1])}

        # столбец с названием средства называется "Название"
        product_name_col_name = "Название"

        # # Собираем дополнительную информацию для каждого средства из листа "Средства"
        # # Ключ — название средства, значение — словарь с данными (цена, бренд, и т.д.)
        additional_info = {}
        for row in range(2, ws.max_row + 1):
            prod_name = ws.cell(row=row, column=headers[product_name_col_name]).value
            if not prod_name:
                continue
            # Собираем данные для всех столбцов, кроме колонки с названием продукта
            row_info = {header: ws.cell(row=row, column=col).value
                        for header, col in headers.items() if header != product_name_col_name}
            additional_info[prod_name] = row_info

        # Обновляем основной словарь, дополняя данные для каждого средства из листа "Средства"
        for prod_name in data.keys():
            # Пропускаем ключ "итоговая рекомендация"
            if prod_name == "Итоговая рекомендация":
                continue
            if prod_name in additional_info:
                data[prod_name].update(additional_info[prod_name])

        return data
