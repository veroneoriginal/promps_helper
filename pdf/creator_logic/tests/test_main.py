# pylint: disable=C0301:: line-too-long
import unittest

from pdf.creator_logic.main import PDFCreator
# from pdf.tests.tests_analogue.data_example import TEST_ANALOGUE_EXPECTED_RESULT
# from pdf.tests.tests_analysis_composition_one_product.with_out_category_data_example import (
#     TEST_ANALYSIS_COMPOSITION_ONE_PRODUCT_WITHOUT_CATEGORY_EXPECTED_RESULT
# )
from pdf.tests.tests_best_combination.data_example import TEST_BEST_COMBINATION_EXPECTED_RESULT
# from pdf.tests.tests_best_couple.data_example import TEST_BEST_COUPLE_EXPECTED_RESULT
#
#
# from pdf.tests.tests_best_product.data_example import (
#     TEST_BEST_PRODUCT_EXPECTED_RESULT,
# )
# from pdf.tests.test_best_product_without_carcinogens.data_example import (
#     TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_EXPECTED_RESULT,
# )


class TestPDFCreator(unittest.TestCase):
    """ Тесты создания pdf-документа """

    def test_create_pdf(self):
        creator = PDFCreator(
            data_for_pdf=TEST_BEST_COMBINATION_EXPECTED_RESULT
        )
        creator.create_pdf()
