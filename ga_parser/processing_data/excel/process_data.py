""" Работа с книгой Excel """

from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.styles import PatternFill


class ExcelProcess:
    """
    Обработка данных о средствах в таблице Excel
    """

    def __init__(
            self,
            excel_file_path: Path,
            ws_title: str,
    ):
        """
        :param excel_file_path: путь к файлу с книгой Excel
        :param ws_title: имя рабочего листа с средствами в книге Excel
        """

        self.excel_file_path: Path = excel_file_path
        self.wb = load_workbook(filename=excel_file_path)
        self.ws = self.wb[ws_title]

    def check_products_dublicates(self):
        """
        Проверяем дубликаты по ссылке или названии,
        если есть - закрашиваем красным строки
        """

        # Загружаем данные первых двух колонок в DataFrame
        df = pd.read_excel(
            io=self.excel_file_path,
            sheet_name=self.ws.title,
            usecols=["Ссылка в Золотом Яблоке", "Артикул в Золотом Яблоке"]
        )

        # Получаем названия колонок
        column_1, column_2 = df.columns

        # Очистка данных
        df[column_1] = df[column_1].astype(str).str.strip().replace("nan", "").replace("", pd.NA)
        df[column_2] = df[column_2].astype(str).str.strip().replace("nan", "").replace("", pd.NA)

        # Фильтруем NaN перед поиском дубликатов
        duplicates_1 = df[column_1].duplicated(keep=False) & df[column_1].notna()
        duplicates_2 = df[column_2].duplicated(keep=False) & df[column_2].notna()

        # Проходим по строкам и выделяем дубликаты
        for row in range(2, len(df) + 2):
            if duplicates_1.iloc[row - 2] or duplicates_2.iloc[row - 2]:
                self.set_row_color(
                    row=self.ws[row],
                    color="FF0000"
                )

        if duplicates_1.any() or duplicates_2.any():
            self.wb_save()
            return True
        return False

    def get_products_for_parse(self) -> dict[str, tuple]:
        """
        Возвращает строки с средствами и книгу Excel,
        которые необходимо спарсить и обновить

        :return: словарь с ссылками на средства и
        кортежами ячеек (каждый кортеж ячеек это строка)
        """

        products_for_parse = {}

        # Проходим по строкам в таблице
        for row in self.ws.iter_rows(min_row=2, max_col=self.ws.max_column, values_only=False):
            product_link = self._check_status(row=row)
            if product_link:
                products_for_parse[product_link] = row

        return products_for_parse

    def _check_status(self, row: tuple) -> str | None:
        """
        Если средство в таблице необходимо обновить - возвращает ссылку на средство

        :param row: строка
        :return: ссылка на товар в Золотом яблоке
        """

        status = self._get_cell_value_in_row_by_title(
            title='Заполнено',
            row=row
        )
        product_link = self._get_cell_value_in_row_by_title(
            title='Ссылка в Золотом Яблоке',
            row=row
        )

        if status != 'да' and product_link:
            return product_link
        return None

    def _get_cell_in_row_by_title(
            self,
            title: str,
            row: tuple
    ) -> Cell | None:
        """
        Находит ячейку строки по названию столбца

        :param title: название столбца
        :param row: кортеж с ячейками строки

        :return: объект-ячейку или None
        """
        title_row = self.ws[1]  # первая строка с заголовками столбцов
        for cell in title_row:
            value = cell.value
            if not value:
                continue
            if cell.value.lower().strip() == title.lower().strip():
                return row[cell.column - 1]
        return None

    def _get_cell_value_in_row_by_title(
            self,
            title: str,
            row: tuple
    ) -> str | None:
        """
        Возвращает значение ячейки строки по названию столбца

        :param title: название столбца
        :param row: кортеж с ячейками строки

        :return: значение ячейки
        """
        cell = self._get_cell_in_row_by_title(title, row)
        val = cell.value
        if val is not None:
            return val.strip().lower()
        return val

    def _set_cell_value_in_row_by_title(
            self,
            title: str,
            row: tuple,
            value: str | int | float,
    ) -> None:
        """
        Записывает значение в ячейку конкретной строки по названию столбца

        :param title: название столбца
        :param row: кортеж с ячейками строки
        :param value: значение ячейки

        :return: None
        """

        cell = self._get_cell_in_row_by_title(title, row)
        if cell:
            cell.value = value
            if not value:
                self.set_cell_color(cell=cell)

    def set_cell_color(
            self,
            cell: Cell,
            color: str = 'FF0000'
    ) -> None:
        """
        Красит ячейку в указанный цвет

        :param cell: ячейка
        :param color: цвет
        """

        cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    def set_row_color(self, row: tuple, color: str = 'FFFF00') -> None:
        """
        Красит все ячейки строки в указанный цвет

        :param row: строка с ячейками
        :param color: цвет
        """
        for cell in row:
            self.set_cell_color(cell=cell, color=color)

    def set_cells_values_in_row_by_title_from_dict(
            self,
            product_data: dict,
            row: tuple,
    ) -> None:
        """
        Записывает значение в ячейку конкретной строки по названию столбца

        :param product_data: словарь с данными по средству
        :param row: кортеж с ячейками строки

        :return: None
        """

        if None in product_data.values():
            self.set_row_color(row=row)

        for k, v in product_data.items():
            self._set_cell_value_in_row_by_title(
                title=k,
                value=v,
                row=row
            )

    def wb_close(self) -> None:
        """
        Сохраняет и закрывает книгу Excel
        """

        self.wb.save(self.excel_file_path)
        self.wb.close()

    def wb_save(self) -> None:
        """
         Сохраняет книгу Excel
        """

        self.wb.save(self.excel_file_path)
