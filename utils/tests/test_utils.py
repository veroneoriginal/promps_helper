"""В этом модуле тестируем выбор json-схемы"""

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

    def setUp(self):
        self.control_manager = ControlManager(
            scheme_for_folders=scheme_for_folders_name,
            param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES
        )

    # def test__take_data_from_table_tool(self):
    #     """
    #     Расшифровка данных из словаря текущей подборки
    #     """
    #     data_tools = self.control_manager._take_data_from_table_tool(
    #         file_path_tools_table=file_path_tools,
    #     )
    #     pprint(data_tools)

    # def test_get_count_collections(self):
    #     """
    #     Подсчет количества незаполненных подборок в таблице.
    #     """
    #
    #     result = self.control_manager._get_count_collections(file_path_collection)
    #     self.assertEqual(2, result)

    # def test_take_data_from_collection(self):
    #     """
    #     Формирование словаря с подборкой
    #     """
    #
    #     result = self.control_manager._take_data_from_collection(file_path_collection)
    #
    #     # Если код "Лучшее средство"
    #     # result = {
    #     #     'Содержимое': 'Шампуни',
    #     #     'Пол': 'женский',
    #     #     'Возраст': '32',
    #     #     'Тип': ('В1', 'В10'),
    #     #     'Запрос': 'ЗВ8, ЗВ12',
    #     #     'Задача': 'Лучшее средство',
    #     #     'Специалист': 'Т',
    #     #     'Средства': (
    #     #         'ALTEREGO ITALY Curego Hydraday',
    #     #         'LADOR Keratin LPP',
    #     #         'NATURA SIBERICA Oblepikha',
    #     #         'OUSHEN Curl & shine shampoo',
    #     #         'PAYOT Shampoing doux biome-friendly',
    #     #         'WELEDA Millet Nourishing'),
    #     #     'Лучший вариант': None,
    #     #     'Итог': None,
    #     #     'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
    #     # }
    #
    #     print(result)

    def test_creating_a_dict_info_for_json_schema_prompts_images(self):
        """
        Формирование словаря с информацией для json-схемы, для промпта и для картинок
        """

        # Если код "Лучшее средство"
        data_collection = {
            'Содержимое': 'Шампуни',
            'Пол': 'женский',
            'Возраст': '32',
            'Тип': ('В1', 'В10'),
            'Запрос': 'ЗВ8, ЗВ12',
            'Задача': 'Лучшее средство',
            'Специалист': 'Т',
            'Средства': (
                'ALTEREGO ITALY Curego Hydraday',
                'LADOR Keratin LPP',
                'NATURA SIBERICA Oblepikha',
                'OUSHEN Curl & shine shampoo',
                'PAYOT Shampoing doux biome-friendly',
                'WELEDA Millet Nourishing'),
            'Лучший вариант': None,
            'Итог': None,
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
        }

        result = {
            # определяем задачу для выбора в json-схемы
            "Задача": data_collection['Задача'],
            # считаем сколько средств подаем для анализа
            "Количество элементов": len(data_collection['Средства']),
            "Категория": data_collection['Содержимое']
        }

        print(result)

        # result = {
        #     'Задача': 'Лучшее средство',
        #     'Количество элементов': 6,
        #     'Категория': 'Шампуни'
        # }



    def test_decrypting_data_from_current_collection(self):
        """
        Обновление словаря с текущей подборкой расшифрованными данными
        """

        # Если код "Лучшее средство"
        data_collection = {
            'Содержимое': 'Шампуни',
            'Пол': 'женский',
            'Возраст': '32',
            'Тип': ('В1', 'В10'),
            'Запрос': 'ЗВ8, ЗВ12',
            'Задача': 'Лучшее средство',
            'Специалист': 'Т',
            'Средства': (
                'ALTEREGO ITALY Curego Hydraday',
                'LADOR Keratin LPP',
                'NATURA SIBERICA Oblepikha',
                'OUSHEN Curl & shine shampoo',
                'PAYOT Shampoing doux biome-friendly',
                'WELEDA Millet Nourishing'),
            'Лучший вариант': None,
            'Итог': None,
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
        }

