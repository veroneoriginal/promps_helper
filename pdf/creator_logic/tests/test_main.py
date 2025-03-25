import unittest

from pdf.creator_logic.main import PDFCreator
from pdf.tests.tests_best_product.data_example import TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT


class TestPDFCreator(unittest.TestCase):
    """ Тесты создания pdf-документа """

    def test_create_pdf(self):
        creator = PDFCreator(collection_data=TEST_BEST_PRODUCT_EXPECTED_RESULT_BEST_PRODUCT)
        creator.create_pdf()
