# pylint: skip-file
import unittest
from pathlib import Path

from pdf.creator_logic.creator.document_creator import PDFConverterToImage

input_data = {
    Path(
        '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/alterego_italy_scalpego_balancing.pdf'):
        {
            'jpg_file_name': Path(
                '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg/alterego_italy_scalpego_balancing.jpg'),
            'size': (1024, 1280)
        },
    Path(
        '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/loreal_professionnel_serioxyl_advanced.pdf'):
        {
            'jpg_file_name': Path(
                '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg/loreal_professionnel_serioxyl_advanced.jpg'),
            'size': (1024, 1280)
        },
    Path('01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/natura_siberica_oblepikha.pdf'):
        {
            'jpg_file_name': Path(
                '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg/natura_siberica_oblepikha.jpg'),
            'size': (1024, 1280)
        }
}


class TestPDFConverterToImage(unittest.TestCase):
    """ Тесты конвертации pdf-документов в JPEG """

    def test_create_pdf(self):
        converter = PDFConverterToImage(file_paths=input_data)
        converter.convert_to_image()
