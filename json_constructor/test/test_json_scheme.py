# pylint: skip-file
"""В этом модуле тестируем выбор json-схемы"""

import unittest
from pprint import pprint

from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES


class TestJsonScheme(unittest.TestCase):

    def test_decryption_task_best_product(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшее средство'.
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                         'Средство_2': 'OUSHEN Curl & shine shampoo',
                         'Средство_3': 'NATURA SIBERICA Oblepikha',
                         'Средство_4': 'WELEDA Millet Nourishing',
                         'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                         'Средство_6': 'LADOR Keratin LPP'},
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

        json_proc_data = JsonProcessingData(data_collection=data_collection)
        result = json_proc_data.distribution_on_task()
        pprint(result)



        # получаем
        # result =  {'Возраст': 32,
        #  'Задача': 'Лучшее средство',
        #  'Запрос': 'ЗВ8, ЗВ12',
        #  'Итог': None,
        #  'Количество средств': 6,
        #  'Лучший вариант': None,
        #  'Пол': 'женский',
        #  'Категория': 'Шампуни',
        #  'Специалист': 'Т',
        #  'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
        #               'Средство_2': 'OUSHEN Curl & shine shampoo',
        #               'Средство_3': 'NATURA SIBERICA Oblepikha',
        #               'Средство_4': 'WELEDA Millet Nourishing',
        #               'Средство_5': 'PAYOT Shampoing doux biome-friendly',
        #               'Средство_6': 'LADOR Keratin LPP'},
        #  'Тип': 'В1, В10',
        #  'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

    def test_decryping_task_one_product(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшее средство'.
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Разбор состава одного средства',
            'Запрос': 'ЗЛ2',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'уход за кожей лица',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'КЛ1',
            'Хеш': '1cf5f44310b2ea42c5b498aef5a314dcea315cf69f4a6d97c96101ea8e517229'
        }

        json_proc_data = JsonProcessingData(data_collection=data_collection)
        update_data_collection = json_proc_data.distribution_on_task()

        # Создание экземпляра класса по созданию json-схемы
        json_creator = JsonCreator(data_collection=update_data_collection,
                                   product_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES)

        # вызов метода для создания json-схемы
        pprint(json_creator.get_json_scheme_for_distribution_on_task())
