# pylint: skip-file
"""
В этом модуле тестируем логику подготовки данных для создания
PDF-документов в соответствии с задачами
"""

import unittest
from pprint import pprint

from dev_helpers.data_tools_for_test import ALL_DATA_TOOLS_FOR_TEST
from pdf.pdf_data_processing.main import PDFDataProcessor
from pdf.tests.tests_best_combination.data_example import (
    TEST_BEST_COMBINATION_COLLECTION_DATA,
    TEST_BEST_COMBINATION_SELECTION_RESULT,
    TEST_BEST_COMBINATION_PATH_PDF_FILE,
    TEST_BEST_COMBINATION_EXPECTED_RESULT,
)

from pdf.tests.tests_best_product.data_example import (
    TEST_BEST_PRODUCT_COLLECTION_DATA,
    TEST_BEST_PRODUCT_SELECTION_RESULT,
    TEST_BEST_PRODUCT_EXPECTED_RESULT,
    TEST_BEST_PRODUCT_PATH_PDF_FILE,
)
from pdf.tests.tests_analysis_composition_one_product.with_out_category_data_example import (
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_EXPECTED_RESULT,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
)

from pdf.tests.test_best_product_without_carcinogens.data_example import (
    TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_COLLECTION_DATA,
    TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_SELECTION_RESULT,
    TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_EXPECTED_RESULT,
    TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_PDF_FILE,
)


class TestTasksDataProcessing(unittest.TestCase):
    """ Тесты подготовки данных в задачах """

    def test_best_product_task_main(self):
        """
        Задача "Лучшее средство", полное формирование данных
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_BEST_PRODUCT_COLLECTION_DATA,
            info_data=ALL_DATA_TOOLS_FOR_TEST,
            selection_result=TEST_BEST_PRODUCT_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_BEST_PRODUCT_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        # pprint(result)
        self.maxDiff = None
        self.assertListEqual(result, TEST_BEST_PRODUCT_EXPECTED_RESULT)

    def test_best_product_without_carcinogens_main(self):
        """
        Задача "Лучшее средство без канцерогенов", полное формирование данных
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_COLLECTION_DATA,
            info_data=ALL_DATA_TOOLS_FOR_TEST,
            selection_result=TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        self.maxDiff = None
        # pprint(result)
        self.assertListEqual(result, TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_EXPECTED_RESULT)

    def test_analysis_composition_one_product_shampoo(self):
        """
        Задача "Разбор состава одного средства"
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
            info_data=ALL_DATA_TOOLS_FOR_TEST,
            selection_result=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        self.maxDiff = None
        self.assertListEqual(result, TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_EXPECTED_RESULT)

    def test_best_combination(self):
        """
        Задача "Лучшее сочетание"
        """
        data_processor = PDFDataProcessor(
            collection_data=TEST_BEST_COMBINATION_COLLECTION_DATA,
            info_data=ALL_DATA_TOOLS_FOR_TEST,
            selection_result=TEST_BEST_COMBINATION_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_BEST_COMBINATION_PATH_PDF_FILE,
        )
        result = data_processor.process_data_with_task_code()
        self.maxDiff = None
        self.assertListEqual(result, TEST_BEST_COMBINATION_EXPECTED_RESULT)
