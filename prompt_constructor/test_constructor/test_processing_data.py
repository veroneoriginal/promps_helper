# pylint: disable=C0301: line-too-long
import unittest

from prompt_constructor.prompt_processing_data import PromptProcessingData
from prompt_constructor.test_constructor.constants_for_tests import (
    BEST_SET_DECRYPED,
    DECRYPT_BEST_PROD,
    DECRYPT_BEST_ONE_PROD,
)
# pylint: disable=E0611: no-name-in-module
from dev_helpers.data_tools_for_test import ALL_DATA_TOOLS_FOR_TEST


class TestProcessingData(unittest.TestCase):
    """
    Тесты на проверку работы первого этапа / ProcessingData
    """

    def test_decryption_key_best_couple(self):
        """
        Тест для расшифровки ключа средства для кода задачи 'Лучшая пара'.
        Проверка работы функции - decrypting_best_set.
        """
        # текущая подборка
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшая пара',
            'Запрос': 'ЗВ8, ЗВ12',
            'Категория': 'Шампуни',
            'Количество наборов': 2,
            'Количество средств в наборе': 2,
            'Пол': 'женский',
            'Путь': None,
            'Специалист': 'Т',
            'Средства': {'Набор_1': {'Средство_1': ('R+CO Dallas Biotin Thickening Shampoo', '24320200017'),
                                     'Средство_2': ('R+CO TELEVISION Perfect Hair Masque', '19760310342')},
                         'Набор_2': {'Средство_1': ('R+CO Atlantis Moisturizing B5 Shampoo', '24320200015'),
                                     'Средство_2': ('R+CO Television Perfect Hair Conditioner', '24320100036')}},
            'Тип': 'В1, В10',
            'Хеш': 'cfc392bfd045eb548d8989bb96c1ac57385a16a804291d38f93415ac1ae340d1'}

        prompt_proces_data = PromptProcessingData(
            data_tools=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_best_couple(
            data=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )
        print(decrypted_products)
        self.maxDiff = None
        self.assertEqual(decrypted_products, BEST_SET_DECRYPED)

    def test_decryption_key_best_prod(self):
        """
        Тест для расшифровки ключа средства для кода задачи
        'Лучшее средство без канцерогенов'

        Проверка работы функции - decrypting_info_code_best_product.
        """

        # текущая подборка
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство без канцерогенов',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': ('OUSHEN Curl & shine shampoo', '19000220056'),
                         'Средство_2': ('NATURA SIBERICA Oblepikha', '19000141580'),
                         'Средство_3': ('ALTEREGO ITALY Curego Hydraday', '19000222487')},
            'Тип': 'В1, В10',
            'Хеш': 'cdd6f7ca257e7f4fc9fa309bce83f7a0c3527b94d576daa29e0f1fac523b6259'}

        prompt_proces_data = PromptProcessingData(
            data_tools=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_info_code_best_product(
            data=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )
        self.assertEqual(decrypted_products.strip(), DECRYPT_BEST_PROD.strip())

    def test_decryption_key_one_prod(self):
        """
        Тест для расшифровки ключа средства для кода задачи
       'Разбор состава одного средства'

        Проверка работы функции - decrypting_info_code_best_product.
        """
        # текущая подборка
        data_collection = {
            'Возраст': 32,
            'Задача': 'Разбор состава одного средства',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'Шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487')},
            'Тип': 'В1, В10',
            'Хеш': 'cdd6f7ca257e7f4fc9fa309bce83f7a0c3527b94d576daa29e0f1fac523b6259'}

        prompt_proces_data = PromptProcessingData(
            data_tools=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_info_code_best_product(
            data=ALL_DATA_TOOLS_FOR_TEST,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )

        self.assertEqual(decrypted_products.strip(), DECRYPT_BEST_ONE_PROD.strip())
