import unittest

from ga_parser.utils.utils import add_text_to_image


class UtilsTestCase(unittest.TestCase):

    def test_add_text_to_image(self):
        """
        Проверка нанесения текста на изображение
        """

        file_name = 'alterego_italy_scalpego_balancing.jpg'
        open_full_path = f'ga_parser/utils/tests/{file_name}'
        name, extension = file_name.split('.')
        save_full_path = f'ga_parser/utils/tests/{name}_with_text.{extension}'

        print('Добавил надпись на изображение. Сохранил в ')
        add_text_to_image(
            open_full_path=open_full_path,
            save_full_path=save_full_path,
            text='Источник: https://goldapple.ru/19000351723-no-1',
        )
