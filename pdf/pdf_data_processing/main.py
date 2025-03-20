# pylint: disable=E0611: no-name-in-module
from pdf.pdf_data_processing.tasks_logic.best_product.main import best_product_task_main


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
        Возвращает словарь с готовой информацией по подборке,
        для передачи в PDFCreator для создания PDF и изображений

        :return: dict
        """

        task = self.collection_data['Задача']
        return self.method_for_task_code[task]()

    def _least_similar(self):
        """ Наименее похож """

    def _most_similar(self):
        """ Наиболее похож """

    def _analogue(self):
        """ Аналог """

    def _best_layout(self):
        """ Лучшая компоновка """

    def _best_combination(self):
        """ Лучшее сочетание """

    def _best_para(self):
        """ Лучшая пара """

    def _analysis_composition_one_product(self):
        """
        Разбор состава одного средства
        """

    def _best_product_without_carcinogens(self):
        """
        Лучшее средство без канцерогенов
        """

    def _best_product(self):
        """
        Лучшее средство
        """

        return best_product_task_main(
            collection_data=self.collection_data,
            info_data=self.info_data,
            selection_result=self.selection_result,
            path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
        )
