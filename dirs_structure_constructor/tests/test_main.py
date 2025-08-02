import unittest
from unittest.mock import patch

from dirs_structure_constructor.main import DirsConstructor

data_collection = {
    'Категория': 'Шампуни'
}

path_to_output_folder = '01_test_base/00_info_for_post/'

SCHEME_FOR_FOLDERS_NAME = {
    '00_source': ['00_json_scheme', '01_prompt', '02_answer_gpt', '03_pdf', '04_jpg', '05_text'],
    '01_telegram': ['00_jpg', '01_text'],
    '02_instagram': ['00_jpg', '01_text'],
    '03_pinterest': ['00_jpg'],
}


class TestDirsConstructor(unittest.TestCase):
    """ Тесты получения путей папок для сохранения """

    @patch("dirs_structure_constructor.main.datetime")
    def test_get_dir_paths(self, mock_datetime):
        """
        Получаем пути
        """

        mock_datetime.now.return_value.strftime.return_value = "12_12_2222"
        dirs_constructor = DirsConstructor(
            base_output_folder_path=path_to_output_folder,
            scheme_for_folders_name=SCHEME_FOR_FOLDERS_NAME,
            data_collection=data_collection
        )
        dirs_constructor.get_output_folders(prefix=data_collection['Группа'])
