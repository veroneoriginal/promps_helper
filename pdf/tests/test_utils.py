# pylint: skip-file
import unittest
from pathlib import Path
from pprint import pprint

from pdf.tests.data_example import (
    TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT,
    TEST_PATH_TO_OUTPUT_FOLDER_JPG_FILE,
)
from pdf.utils import _get_pdf_file_paths


class TestUtils(unittest.TestCase):
    """ Тесты вспомогательных функций """

    def test_get_pdf_file_paths(self):
        """
        Создание путей для конвертации PDF в JPEG
        """
        result = _get_pdf_file_paths(
            input_data=TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT['Данные'],
            path_to_output_folder_jpg_file=TEST_PATH_TO_OUTPUT_FOLDER_JPG_FILE
        )


        expected_value = {
            Path(
                '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/alterego_italy_scalpego_balancing.pdf'):
                {
                    'jpg_file_name': Path(
                        '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_JPG/alterego_italy_scalpego_balancing.jpg'),
                    'size': (1024, 1280)
                },
            Path(
                '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/loreal_professionnel_serioxyl_advanced.pdf'):
                {
                    'jpg_file_name': Path(
                        '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_JPG/loreal_professionnel_serioxyl_advanced.jpg'),
                    'size': (1024, 1280)
                },
            Path('01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/natura_siberica_oblepikha.pdf'):
                {
                    'jpg_file_name': Path(
                        '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_JPG/natura_siberica_oblepikha.jpg'),
                    'size': (1024, 1280)
                }
        }

        self.maxDiff = None
        self.assertDictEqual(result, expected_value)
