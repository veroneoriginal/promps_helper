# pylint: disable=C0301: line-too-long
import unittest

from pdf.main import create_pdf
from pdf.tests.tests_best_product.data_example import (
    TEST_BEST_PRODUCT_INFO_DATA,
    TEST_BEST_PRODUCT_COLLECTION_DATA,
    TEST_BEST_PRODUCT_SELECTION_RESULT,
    TEST_BEST_PRODUCT_PATH_PDF_FILE,
    TEST_BEST_PRODUCT_PATH_JPG_FILE,
)

from pdf.tests.tests_analysis_composition_one_product.with_out_category_data_example import (
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_INFO_DATA,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
    TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_JPG_FILE,
)


class TestCreatePdf(unittest.TestCase):
    """
    Тесты полного цикла создания PDF и изображений из них
    """

    def test_best_product(self):
        """
        Задача "Лучший продукт"
        """
        create_pdf(
            collection_data=TEST_BEST_PRODUCT_COLLECTION_DATA,
            info_data=TEST_BEST_PRODUCT_INFO_DATA,
            selection_result=TEST_BEST_PRODUCT_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_BEST_PRODUCT_PATH_PDF_FILE,
            path_to_output_folder_jpg_file=TEST_BEST_PRODUCT_PATH_JPG_FILE
        )

    def test_analysis_composition_one_product(self):
        """
        Задача "Разбор состава одного средства"
        """
        create_pdf(
            collection_data=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_COLLECTION_DATA,
            info_data=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_INFO_DATA,
            selection_result=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_PDF_FILE,
            path_to_output_folder_jpg_file=TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_PATH_JPG_FILE
        )
