# pylint: skip-file
"""
В этом модуле тестируем логику подготовки данных для создания
PDF-документов в соответствии с задачами
"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager
from pdf.pdf_data_processing.main import PDFDataProcessor
from pdf.pdf_data_processing.tasks_logic.best_product import (
    best_product_get_brand_line_path,
)
from pdf.tests.tests_best_product.data_example import (
    TEST_BEST_PRODUCT_INFO_DATA,
    TEST_BEST_PRODUCT_COLLECTION_DATA,
    TEST_BEST_PRODUCT_SELECTION_RESULT,
    TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT,
    TEST_BEST_PRODUCT_PATH_PDF_FILE,
    FILE_PATH_TOOLS,
)
from pdf.tests.tests_analysis_composition_one_product.with_out_category_data_example import (
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_INFO_DATA,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_EXPECTED_RESULT,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
)

from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES


def get_one_product_dict(product_title: str) -> dict:
    """
    Возвращает словарь с данными по обному средству
    """
    control_manager = ControlManager(
        param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
    )
    data_tools = control_manager._take_data_from_table_tool(
        file_path_tools_table=FILE_PATH_TOOLS,
    )
    return data_tools['Средства'][product_title]


# print(get_one_product_dict(
#     product_title='NATURA SIBERICA Oblepikha'
# ))


class TestTasksDataProcessing(unittest.TestCase):
    """ Тесты подготовки данных в задачах """

    def test_best_product_get_brand_line_color(self):
        """
        Возвращает путь к файлу с нужной бренд-линией для нанесения
        на PDF для задачи "Лучшее средство"
        """

        result = best_product_get_brand_line_path(
            task='Лучшее средство',
            category='Шампуни',
            value=True,
        )
        self.assertIn('border_green.jpg', result)

        result = best_product_get_brand_line_path(
            task='Лучшее средство',
            category='Шампуни',
            value=False,
        )
        self.assertIn('border_fiolet.jpg', result)

    def test_best_product_task_main(self):
        """
        Задача "Лучшее средство", полное формирование данных
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_BEST_PRODUCT_COLLECTION_DATA,
            info_data=TEST_BEST_PRODUCT_INFO_DATA,
            selection_result=TEST_BEST_PRODUCT_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_BEST_PRODUCT_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        self.maxDiff = None
        # pprint(result)
        self.assertDictEqual(result, TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT)


    def test_analysis_composition_one_product_shampoo(self):
        """
        Задача "Разбор состава одного средства"
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
            info_data=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_INFO_DATA,
            selection_result=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        # self.maxDiff = None
        pprint(result)
        # self.assertDictEqual(result, TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT)