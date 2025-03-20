# pylint: disable=E0611: no-name-in-module
from pdf.pdf_data_processing.tasks_logic.analysis_composition_one_product import (
    analysis_composition_one_product_task_main,
)
from pdf.pdf_data_processing.tasks_logic.base_task import process_products_common
from pdf.pdf_data_processing.tasks_logic.best_product import best_product_task_main


class PDFDataProcessor:
    """
    Класс для подготовки данных к передаче в PDFCreator
    """

    def __init__(
            self,
            collection_data: dict,
            info_data: dict,
            selection_result: dict,
            path_to_output_folder_pdf_file: str,

    ) -> None:
        """
        :param collection_data: данные подборки
        :param info_data: данные с всеми средствами, врачами и т.д. (База данных)
        :param selection_result: данные с результатом нейронки по подборке
        :param path_to_output_folder_pdf_file: путь к папке для сохранения pdf-файлов

        :return: None
        """

        self.collection_data = collection_data
        self.info_data = info_data
        self.selection_result = selection_result
        self.path_to_output_folder_pdf_file = path_to_output_folder_pdf_file

        self.method_for_task_code = {
            'Лучшее средство': self._best_product,
            'Лучшее средство без канцерогенов': self._best_product_without_carcinogens,
            'Разбор состава одного средства': self._analysis_composition_one_product,
            'Лучшая пара': self._best_para,
            'Лучшее сочетание': self._best_combination,
            'Лучшая компоновка': self._best_layout,
            'Аналог': self._analogue,
            'Наиболее похож': self._most_similar,
            'Наименее похож': self._least_similar,
        }

    def process_data_with_task_code(self) -> dict:
        """
        Вызывает нужную логику в зависимости от кода задачи
        Возвращает словарь с готовой полной информацией по подборке,
        для передачи в PDFCreator для создания PDF и изображений

        :return: dict
        """

        task = self.collection_data['Задача']
        all_products_data, build_product_data_func = self.method_for_task_code[task]()

        return process_products_common(
            collection_data=self.collection_data,
            info_data=self.info_data,
            all_products_data=all_products_data,
            path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
            build_product_data_func=build_product_data_func
        )

    def _least_similar(self):
        """ Задача "Наименее похож" """

    def _most_similar(self):
        """ Задача "Наиболее похож" """

    def _analogue(self):
        """ Задача "Аналог" """

    def _best_layout(self):
        """ Задача "Лучшая компоновка" """

    def _best_combination(self):
        """ Задача "Лучшее сочетание" """

    def _best_para(self):
        """ Задача "Лучшая пара" """

    def _analysis_composition_one_product(self) -> tuple[list, callable]:
        """
        Задача "Разбор состава одного средства"
        """
        # Готовим список с словарями данных по каждому средству
        # в соответствии с json-схемой задачи
        all_products_data: list[dict] = [self.selection_result, ]

        return all_products_data, analysis_composition_one_product_task_main

    def _best_product_without_carcinogens(self):
        """ Задача "Лучшее средство без канцерогенов" """

    def _best_product(self):
        """ Задача "Лучшее средство" """

        # Готовим список с словарями данных по каждому средству
        # в соответствии с json-схемой задачи
        all_products_data: list[dict] = []

        for key, value in self.selection_result.items():
            if key.startswith('product_'):
                all_products_data.append(value)

        return all_products_data, best_product_task_main
