"""
В этом модуле тестируем выбор json-схемы
"""

import unittest

from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData
from json_constructor.test.constants import (
    EXPECTED_SCHEMA_FOR_BEST_PRODUCT,
    EXPECTED_SCHEMA_FOR_ONE_PRODUCT,
    EXPECTED_SCHEMA_FOR_BEST_PROD_CARCINOGEN,
    BEST_COMBINATION_JSON,
    BEST_SET_JSON,
    EXPECTED_SCHEMA_FOR_ANALOGUE_PRODUCT,
)
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES


class TestJsonScheme(unittest.TestCase):

    def test_decryption_task_best_product(self):
        """
        Проверка работы метода decryption_task_best_product для преобразования
        словаря по коду задачи - 'Лучшее средство'.
        Тест проверяет, что:
        - осуществляется добавление ключа 'Количество средств'
        - правильно считается количество средств
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
            'Средства': {
                'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
                'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
                'Средство_3': ('NATURA SIBERICA Oblepikha', '19000141580'),
                'Средство_4': ('WELEDA Millet Nourishing', '15180100004'),
                'Средство_5': ('PAYOT Shampoing doux biome-friendly', '19000153618'),
                'Средство_6': ('LADOR Keratin LPP', '19760200012')
            },
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

        # Ожидаемое количество ключей ДО обработки
        original_keys_count = len(data_collection.keys())

        # Инициализация объекта и вызов метода
        json_proc_data = JsonProcessingData(data_collection=data_collection)
        result = json_proc_data.decryption_task_best_product(data_collection=data_collection)
        # pprint(result)

        # Ожидаемый результат
        expected_result = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
                         'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
                         'Средство_3': ('NATURA SIBERICA Oblepikha', '19000141580'),
                         'Средство_4': ('WELEDA Millet Nourishing', '15180100004'),
                         'Средство_5': ('PAYOT Shampoing doux biome-friendly', '19000153618'),
                         'Средство_6': ('LADOR Keratin LPP', '19760200012')},
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
            'Количество средств': 6
        }

        # Проверка, что добавился ключ 'Количество средств'
        self.assertIn('Количество средств', result,
                      msg="Отсутствует ключ 'Количество средств'")

        # Проверка, что значение количества средств корректно
        self.assertEqual(result['Количество средств'], 6,
                         msg="Некорректное значение ключа 'Количество средств'")

        # Проверка, что добавился ровно один ключ
        self.assertEqual(len(result.keys()), original_keys_count + 1,
                         msg="Добавилось больше одного нового ключа")

        # Проверка, что результат равен ожидаемому
        self.assertEqual(result, expected_result,
                         msg="Результат обработки не совпадает с ожидаемым словарём")


    def test_get_json_scheme_for_analogue_product(self):
        """
        Проверка корректного формирования json-схемы для задачи 'Аналог'
        """

        # Подготовка данных
        data_collection = {
            'Возраст': 32,
            'Задача': 'Аналог',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {
                'Исходное средство': ('КУДРЯВЫЙ МЕТОД for curly hair № 1', '19000351723'),
                'Аналог средство': ('R+CO Dallas Biotin Thickening Shampoo', '24320200017'),
            },
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
            'Количество средств': 6
        }

        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()
        # pprint(actual_schema)
        # Проверка, что схема совпадает с ожидаемой
        self.assertDictEqual(
            actual_schema,
            EXPECTED_SCHEMA_FOR_ANALOGUE_PRODUCT,
            msg="Схема не совпадает с ожидаемой",
        )

    def test_get_json_scheme_for_best_product(self):
        """
        Проверка корректного формирования json-схемы для задачи 'Лучшее средство'
        """

        # Подготовка данных
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {
                'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
                'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
                'Средство_3': ('NATURA SIBERICA Oblepikha', '19000141580'),
                'Средство_4': ('WELEDA Millet Nourishing', '15180100004'),
                'Средство_5': ('PAYOT Shampoing doux biome-friendly', '19000153618'),
                'Средство_6': ('LADOR Keratin LPP', '19760200012')
            },
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
            'Количество средств': 6
        }

        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()
        # pprint(actual_schema)
        # Проверка, что схема совпадает с ожидаемой
        self.assertDictEqual(
            actual_schema,
            EXPECTED_SCHEMA_FOR_BEST_PRODUCT,
            msg="Схема не совпадает с ожидаемой",
        )

    def test_decryption_task_one_product(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшее средство'
        и получения json-схемы дял категории 'уход за кожей лица'
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Разбор состава одного средства',
            'Запрос': 'ЗЛ2',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Уход за кожей лица',
            'Специалист': 'Т',
            'Средства': {
                'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
            },
            'Тип': 'КЛ1',
            'Хеш': '1cf5f44310b2ea42c5b498aef5a314dcea315cf69f4a6d97c96101ea8e517229'
        }

        # на этом этапе по этому ключу ничего не происходит в функции
        json_proc_data = JsonProcessingData(data_collection=data_collection)
        update_data_collection = json_proc_data.distribution_on_task()

        # Создание экземпляра класса по созданию json-схемы
        json_creator = JsonCreator(
            data_collection=update_data_collection,
            product_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()

        self.maxDiff = None
        # Проверка результата
        self.assertDictEqual(
            actual_schema,
            EXPECTED_SCHEMA_FOR_ONE_PRODUCT,
            msg="Схема не совпадает с ожидаемой",
        )

    def test_get_json_scheme_for_best_product_carcinogen_free(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшее средство без канцерогенов'
        и получения json-схемы дял категории 'уход за кожей лица'
        """
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство без канцерогенов',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'Шампуни',
            'Количество средств': 4,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {
                'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
                'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
                'Средство_3': ('NATURA SIBERICA Oblepikha', '19000141580'),
                'Средство_4': ('WELEDA Millet Nourishing', '15180100004'),
            },
            'Тип': 'В1, В10',
            'Хеш': '15ef9afdd97761bce2a300aa4bd11b74b2117c8dfe15b0f5e92c62af1cbeaf54',
        }
        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()
        # Проверка, что схема совпадает с ожидаемой
        self.assertDictEqual(
            actual_schema,
            EXPECTED_SCHEMA_FOR_BEST_PROD_CARCINOGEN,
            msg="Схема не совпадает с ожидаемой",
        )

    def test_get_json_scheme_for_best_combination(self):
        """
        Проверка работы метода для получения json-схемы
        по коду задачи - 'Лучшее сочетание'
        """
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее сочетание',
            'Запрос': 'ЗВ8, ЗВ12',
            'Исходное средство': 'R+CO Atlantis Moisturizing B5 Shampoo',
            'Итог': None,
            'Категория': 'Шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {
                'Исходное средство': ('R+CO Television Perfect Hair Conditioner', '24320100036'),
                'Средство_2': ('R+CO Atlantis Moisturizing B5 Conditioner', '24320200016'),
                'Средство_3': ('R+CO TELEVISION Perfect Hair Masque', '19760310342'),
            },
            'Тип': 'В1, В10',
            'Хеш': '2d2918a9e091164a303dd3c652d052b2b2bcc3bb88dd7c075a4c8b31aed75b6d',
        }
        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories,
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()
        # Проверка, что схема совпадает с ожидаемой
        self.maxDiff = None
        self.assertDictEqual(
            actual_schema,
            BEST_COMBINATION_JSON,
            msg="Схема не совпадает с ожидаемой",
        )

    def test_get_json_scheme_for_best_couple(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшая пара' и получения json-схемы
        """
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшая пара',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'Шампуни',
            'Количество наборов': 2,
            'Количество средств в наборе': 2,
            'Лучший вариант': 'не работает, ошибка в json схеме',
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {
                'Набор_1':
                    {
                        'Средство_1': ('R+CO Dallas Biotin Thickening Shampoo', '24320200017'),
                        'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
                    },
                'Набор_2':
                    {
                        'Средство_1': ('R+CO Atlantis Moisturizing B5 Shampoo', '24320200015'),
                        'Средство_2': ('R+CO TELEVISION Perfect Hair Conditioner', '24320100036'),
                    }
            },
            'Тип': 'В1, В10',
            'Хеш': 'cfc392bfd045eb548d8989bb96c1ac57385a16a804291d38f93415ac1ae340d1'}

        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories,
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()

        # Проверка, что схема совпадает с ожидаемой
        self.assertDictEqual(
            actual_schema,
            BEST_SET_JSON,
            msg="Схема не совпадает с ожидаемой",
        )
