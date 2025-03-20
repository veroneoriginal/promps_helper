# pylint: skip-file
"""В этом модуле тестируем всю логику работы приложения"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager
from pdf.pdf_data_processing.tasks_logic.best_product.main import (
    best_product_get_brand_line_path,
    best_product_calc_base_price_ratio,
    best_product_task_main,
)
from pdf.tests.data_example import (
    TEST_INFO_DATA,
    TEST_COLLECTION_DATA,
    TEST_SELECTION_RESULT,
    TEST_EXPECTED_RESULT_FROM_PDF_DATA_PROCESSING,
    TEST_PATH_TO_OUTPUT_FOLDER_PDF_FILE,
    FILE_PATH_TOOLS,
)
from source.structure_folders import SCHEME_FOR_FOLDERS_NAME
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


class TestBestProduct(unittest.TestCase):
    """ Тесты подготовки данных в задаче "Лучший продукт" """

    def test_best_product_get_brand_line_color(self):
        """
        Возвращает путь к файлу с нужной бренд-линией для нанесения
        на PDF для задачи "Лучшее средство"
        """

        result = best_product_get_brand_line_path(
            task='Лучшее средство',
            value=True,
        )
        self.assertIn('border_green.jpg', result)

        result = best_product_get_brand_line_path(
            task='Лучшее средство',
            value=False,
        )
        self.assertIn('border_fiolet.jpg', result)

    def test_best_product_calc_base_price_ratio(self):
        """
        Готовит строку 'Количество мера / цена'
        Например: '190 мл / 1612 р.'
        """
        result = best_product_calc_base_price_ratio(product=TEST_INFO_DATA['ALTEREGO ITALY Scalpego Balancing'])
        self.assertEqual('300 мл / 3500 рублей', result)

    def test_best_product_task_main(self):
        """
        Задача "Лучшее средство", полное формирование данных
        """

        result = best_product_task_main(
            collection_data=TEST_COLLECTION_DATA,
            info_data=TEST_INFO_DATA,
            selection_result=TEST_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_PATH_TO_OUTPUT_FOLDER_PDF_FILE,
        )
        self.maxDiff = None
        # pprint(result)
        self.assertDictEqual(result, TEST_EXPECTED_RESULT_FROM_PDF_DATA_PROCESSING)
