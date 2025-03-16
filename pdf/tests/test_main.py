import unittest

from pdf.main import create_pdf
from pdf.tests.data_example import (
    TEST_INFO_DATA,
    TEST_COLLECTION_DATA,
    TEST_SELECTION_RESULT,
    TEST_PATH_TO_OUTPUT_FOLDER_PDF_FILE,
    TEST_PATH_TO_OUTPUT_FOLDER_JPG_FILE,
)


class TestCreatePdf(unittest.TestCase):
    """ Тесты полного цикла создания PDF и изображений из них """

    def test_create_pdf(self):
        create_pdf(
            collection_data=TEST_COLLECTION_DATA,
            info_data=TEST_INFO_DATA,
            selection_result=TEST_SELECTION_RESULT,
            path_to_output_folder_pdf_file=TEST_PATH_TO_OUTPUT_FOLDER_PDF_FILE,
            path_to_output_folder_jpg_file=TEST_PATH_TO_OUTPUT_FOLDER_JPG_FILE
        )
