# pylint: disable=E0611: no-name-in-module
from copy import deepcopy

from pdf.pdf_data_processing.tasks_logic.analogue import AnaloguePDFTemplateCreator
from pdf.pdf_data_processing.tasks_logic.analysis_composition_one_product import (
    AnalisisCompositionProductPDFTemplateCreator,
)
from pdf.pdf_data_processing.tasks_logic.best_combination import (
    BestCombinationProductPDFTemplateCreator,
)
from pdf.pdf_data_processing.tasks_logic.best_couple import BestCouplePDFTemplateCreator
from pdf.pdf_data_processing.tasks_logic.best_product import BestProductPDFTemplateCreator
from pdf.pdf_data_processing.tasks_logic.best_product_without_carcinogens import (
    BestProductWithOutConcerogensPDFTemplateCreator,
)
from pdf.pdf_data_processing.tasks_logic.detailed_analysis_composition import (
    DetailedAnalysisCompositionPDFTemplateCreator,
)
from pdf.pdf_data_processing.tasks_utils import translate_keys_to_rus


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
            'Подробный анализ состава': self._detailed_analysis_composition,
            'Лучшее средство': self._best_product,
            'Лучшее средство без канцерогенов': self._best_product_without_carcinogens,
            'Разбор состава одного средства': self._analysis_composition_one_product,
            'Лучшая пара': self._best_couple,
            'Лучшее сочетание': self._best_combination,
            'Лучшая компоновка': self._best_layout,
            'Аналог': self._analogue,
            'Наиболее похож': self._most_similar,
            'Наименее похож': self._least_similar,
        }

    def process_data_with_task_code(self) -> list:
        """
        Вызывает нужную логику в зависимости от кода задачи
        Возвращает словарь с готовой полной информацией по подборке,
        для передачи в PDFCreator для создания PDF и изображений

        :return: список с итоговыми данными для создания PDF. Каждый элемент списка -
        словарь с данными для создания документа.
        """

        task = self.collection_data['Задача']

        rus_selection_result = translate_keys_to_rus(data=deepcopy(self.selection_result))

        pdf_data_creator_class = self.method_for_task_code[task]()
        pdf_data_creator = pdf_data_creator_class(
            collection_data=self.collection_data,
            info_data=self.info_data,
            rus_selection_result=rus_selection_result,
            path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
        )
        return pdf_data_creator.get_data_for_pdf_docs()

    def _least_similar(self):
        """ Задача "Наименее похож" """

    def _most_similar(self):
        """ Задача "Наиболее похож" """

    def _analogue(self):
        """ Задача "Аналог" """

        return AnaloguePDFTemplateCreator

    def _best_layout(self):
        """ Задача "Лучшая компоновка" """

    def _best_combination(self):
        """ Задача "Лучшее сочетание" """

        return BestCombinationProductPDFTemplateCreator

    def _best_couple(self):
        """ Задача "Лучшая пара" """

        return BestCouplePDFTemplateCreator

    def _analysis_composition_one_product(self) -> callable:
        """
        Задача "Разбор состава одного средства"
        """

        return AnalisisCompositionProductPDFTemplateCreator

    def _best_product_without_carcinogens(self) -> callable:
        """ Задача "Лучшее средство без канцерогенов" """

        return BestProductWithOutConcerogensPDFTemplateCreator

    def _best_product(self) -> callable:
        """ Задача "Лучшее средство" """

        return BestProductPDFTemplateCreator

    def _detailed_analysis_composition(self) -> callable:
        """ Задача "Подробный анализ состава" """

        return DetailedAnalysisCompositionPDFTemplateCreator
