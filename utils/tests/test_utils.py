# pylint: skip-file
"""В этом модуле тестируем всю логику работы приложения"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager
# словарь с данными для формирования путей для сохраненяи данных
from source.structure_folders import scheme_for_folders_name
# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES
from utils.utils import decrypting_data_from_current_collection

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

    # def test_get_count_collections(self):
    #     """
    #     Подсчет количества незаполненных подборок в таблице.
    #     """
    #
    #     result = self.control_manager._get_count_collections(file_path_collection)
    #     self.assertEqual(2, result)

    def test_take_data_from_collection(self):
        """
        Формирование словаря с подборкой
        """

        result = self.control_manager._take_data_from_collection(
            file_path_collection=file_path_collection,
            cheking_unique=False,
        )

        # Если код "Лучшее средство"
        # result = {
        #  'Возраст': 32,
        #  'Задача': 'Лучшее средство',
        #  'Запрос': 'ЗВ8, ЗВ12',
        #  'Итог': None,
        #  'Лучший вариант': None,
        #  'Пол': 'женский',
        #  'Содержимое': 'Шампуни',
        #  'Специалист': 'Т',
        #  'Средства': '{\n'
        #              '«Средство_1» : «ALTEREGO ITALY Curego Hydraday»,\n'
        #              '«Средство_2» : «OUSHEN Curl & shine shampoo»,\n'
        #              '«Средство_3» : «NATURA SIBERICA Oblepikha»,\n'
        #              '«Средство_4» : «WELEDA Millet Nourishing»,\n'
        #              '«Средство_5» : «PAYOT Shampoing doux biome-friendly»,\n'
        #              '«Средство_6» : «LADOR Keratin LPP»\n'
        #              '}',
        #  'Тип': 'В1, В10',
        #  'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'
        #  }

        # Разбор состава одного средства
        #   result = {
        #   'Возраст': 32,
        #  'Задача': 'Разбор состава одного средства',
        #  'Запрос': 'ЗЛ2',
        #  'Итог': None,
        #  'Лучший вариант': None,
        #  'Пол': 'женский',
        #  'Содержимое': 'уход за кожей лица',
        #  'Специалист': 'Т',
        #  'Средства': '{\n«Средство_1» : «ALTEREGO ITALY Curego Hydraday»\n}',
        #  'Тип': 'КЛ1',
        #  'Хеш': '1cf5f44310b2ea42c5b498aef5a314dcea315cf69f4a6d97c96101ea8e517229'
        #  }

        pprint(result)



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
         'Содержимое': 'Шампуни',
         'Специалист': 'Т',
         'Средства': '{\n'
                     '«Средство_1» : «ALTEREGO ITALY Curego Hydraday»,\n'
                     '«Средство_2» : «OUSHEN Curl & shine shampoo»,\n'
                     '«Средство_3» : «NATURA SIBERICA Oblepikha»,\n'
                     '«Средство_4» : «WELEDA Millet Nourishing»,\n'
                     '«Средство_5» : «PAYOT Shampoing doux biome-friendly»,\n'
                     '«Средство_6» : «LADOR Keratin LPP»\n'
                     '}',
         'Тип': 'В1, В10',
         'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'
         }

        self.control_manager._get_output_folders(
            path_to_output_folder=path_to_output_folder,
            category=data_collection['Содержимое'],
        )
        pprint(self.control_manager.paths_to_folders)
        # получается
        # {'answer_gpt': '00_base/00_info_for_post/16_03_25/1_Шампуни/answer_gpt',
        #  'instagram_jpg': '00_base/00_info_for_post/16_03_25/1_Шампуни/instagram/jpg',
        #  'instagram_text': '00_base/00_info_for_post/16_03_25/1_Шампуни/instagram/text',
        #  'pinterest_jpg': '00_base/00_info_for_post/16_03_25/1_Шампуни/pinterest/jpg',
        #  'prompt': '00_base/00_info_for_post/16_03_25/1_Шампуни/prompt',
        #  'telegram_jpg': '00_base/00_info_for_post/16_03_25/1_Шампуни/telegram/jpg',
        #  'telegram_pdf': '00_base/00_info_for_post/16_03_25/1_Шампуни/telegram/pdf',
        #  'telegram_text': '00_base/00_info_for_post/16_03_25/1_Шампуни/telegram/text'}



