# pylint: skip-file

"""В этом модуле тестируем всю логику работы приложения"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager

# словарь с данными для формирования путей для сохраненяи данных
from source.structure_folders import scheme_for_folders_name

# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

file_path_tools = '00_base/Средства.xlsx'
file_path_collection = '00_base/Подборки для тестов.xlsx'
path_to_output_folder = '00_base/00_info_for_post/'


class TestUtils(unittest.TestCase):
    """Класс для тестирования всей логики работы приложения"""

    def setUp(self):
        self.control_manager = ControlManager(
            scheme_for_folders=scheme_for_folders_name,
            param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES
        )

        self.data_tools = self.control_manager._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )

    # def test__take_data_from_table_tool(self):
    #     """
    #     Расшифровка данных из словаря текущей подборки
    #     """
    #     data_tools = self.control_manager._take_data_from_table_tool(
    #         file_path_tools_table=file_path_tools,
    #     )
    #     pprint(data_tools)

    def test_get_count_collections(self):
        """
        Подсчет количества незаполненных подборок в таблице.
        """

        result = self.control_manager._get_count_collections(file_path_collection)
        self.assertEqual(2, result)

    def test_take_data_from_collection(self):
        """
        Формирование словаря с подборкой
        """

        result = self.control_manager._take_data_from_collection(
            file_path_collection=file_path_collection,
            checking_unique=False,
        )

        # pprint(result)

        if result['Задача'] == 'Лучшее средство':
            # Если код "Лучшее средство", то ожидаемый словарь имеет вид
            expected_result = {
                'Возраст': 32,
                'Задача': 'Лучшее средство',
                'Запрос': 'ЗВ8, ЗВ12',
                'Итог': None,
                'Лучший вариант': None,
                'Пол': 'женский',
                'Категория': 'шампуни',
                'Специалист': 'Т',
                'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                             'Средство_2': 'OUSHEN Curl & shine shampoo',
                             'Средство_3': 'NATURA SIBERICA Oblepikha',
                             'Средство_4': 'WELEDA Millet Nourishing',
                             'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                             'Средство_6': 'LADOR Keratin LPP'},
                'Тип': 'В1, В10',
                'Хеш': '68dd4868b0ba1a96e83295d05327e97af4f2748a34fb45281023729d8532c326'}

            # Проверка, что результат равен ожидаемому
            self.assertEqual(result, expected_result)

        elif result['Задача'] == 'Разбор состава одного средства':
            expected_result = {
                'Возраст': 32,
                'Задача': 'Разбор состава одного средства',
                'Запрос': 'ЗЛ2',
                'Итог': None,
                'Категория': 'уход за кожей лица',
                'Лучший вариант': None,
                'Пол': 'женский',
                'Специалист': 'Т',
                'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday'},
                'Тип': 'КЛ1',
                'Хеш': '1c1642426270e8bfe75322817e7c2995adde4627fe2b16cb989d89ae8d9ed034'}

            # Проверка, что результат равен ожидаемому
            self.assertEqual(result, expected_result)

    def test_get_output_folders(self):
        """
        Формирование путей для сохранения данных
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                         'Средство_2': 'OUSHEN Curl & shine shampoo',
                         'Средство_3': 'NATURA SIBERICA Oblepikha',
                         'Средство_4': 'WELEDA Millet Nourishing',
                         'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                         'Средство_6': 'LADOR Keratin LPP'},
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

        self.control_manager._get_output_folders(
            path_to_output_folder=path_to_output_folder,
            category=data_collection['Категория'],
        )
        folders = self.control_manager.paths_to_folders

        expected_keys = [
            'answer_gpt',
            'instagram_jpg',
            'instagram_text',
            'pinterest_jpg',
            'prompt',
            'telegram_jpg',
            'telegram_pdf',
            'telegram_text'
        ]

        self.assertCountEqual(folders.keys(), expected_keys)

        # получатся пути такого плана
        # {'answer_gpt': '00_base/00_info_for_post/17_03_25/3_шампуни/answer_gpt',
        #  'instagram_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/instagram/jpg',
        #  'instagram_text': '00_base/00_info_for_post/17_03_25/3_шампуни/instagram/text',
        #  'pinterest_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/pinterest/jpg',
        #  'prompt': '00_base/00_info_for_post/17_03_25/3_шампуни/prompt',
        #  'telegram_jpg': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/jpg',
        #  'telegram_pdf': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/pdf',
        #  'telegram_text': '00_base/00_info_for_post/17_03_25/3_шампуни/telegram/text'}
