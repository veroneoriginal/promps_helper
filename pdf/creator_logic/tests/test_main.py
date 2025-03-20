import unittest

from pdf.creator_logic.main import PDFCreator
from pdf.tests.data_example import TEST_EXPECTED_RESULT_FROM_PDF_DATA_PROCESSING


class TestPDFCreator(unittest.TestCase):
    """ Тесты создания pdf-документа """

    def test_create_pdf(self):
        creator = PDFCreator(collection_data=TEST_EXPECTED_RESULT_FROM_PDF_DATA_PROCESSING)
        creator.create_pdf()
