# pylint: skip-file

"""В этом модуле тестируем всю логику работы приложения"""

import unittest
from pprint import pprint

from control_manager.control_manager import ControlManager

# словарь с данными для формирования путей для сохраненяи данных
from source.structure_folders import SCHEME_FOR_FOLDERS_NAME

# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

file_path_tools = '00_base/Средства.xlsx'
file_path_collection = '00_base/Подборки для тестов.xlsx'
path_to_output_folder = '00_base/00_info_for_post/'


class TestUtils(unittest.TestCase):
    """Класс для тестирования всей логики работы приложения"""

    def setUp(self):
        self.control_manager = ControlManager(
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
        self.assertEqual(3, result)

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
                'Средства': {'Средство_1': 'PULANNA Bio-gold & Grape'},
                'Тип': 'КЛ1, КЛ2',
                'Хеш': '5be8b5391782b170c129765d1b7500816e2309aa682d468f368ffb8cfaa02d40',
            }

            # Проверка, что результат равен ожидаемому
            self.assertEqual(result, expected_result)
