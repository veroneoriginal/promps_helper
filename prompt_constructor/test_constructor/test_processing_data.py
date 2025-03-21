import unittest
from prompt_constructor.prompt_processing_data import PromptProcessingData
from prompt_constructor.test_constructor.constants import (
    best_set_decryped,
    decrypt_best_prod,
    decrypt_best_one_prod,
)
from prompt_constructor.test_constructor.data_tools import data_tools


class TestProcessingData(unittest.TestCase):
    """
    Тесты на проверку работы первого этапа / ProcessingData
    """

    def test_decryption_key_best_set(self):
        """
        Тест для расшифровки ключа средства для кода задачи 'Лучший набор'.
        Проверка работы функции - decrypting_best_set.
        """
        # текущая подборка
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучший набор',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'Шампуни',
            'Количество пар': 2,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {
                'Пара_1':
                    {'Средство_1': 'R+CO Dallas Biotin Thickening Shampoo',
                     'Средство_2': 'R+CO TELEVISION Perfect Hair Masque'},
                'Пара_2':
                    {'Средство_1': 'R+CO Atlantis Moisturizing B5 Shampoo',
                     'Средство_2': 'R+CO Television Perfect Hair Conditioner'}
            },
            'Тип': 'В1, В10',
            'Хеш': '18f0117c05399c5e88d3fa97931d4f0ec183260f09c49a0e6aabe61489efd544'}

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_best_set(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )

        self.assertEqual(decrypted_products.strip(), best_set_decryped.strip())

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
            'Средства': {'Средство_1': 'OUSHEN Curl & shine shampoo',
                         'Средство_2': 'NATURA SIBERICA Oblepikha',
                         'Средство_3': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'В1, В10',
            'Хеш': 'cdd6f7ca257e7f4fc9fa309bce83f7a0c3527b94d576daa29e0f1fac523b6259'}

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_info_code_best_product(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )

        self.assertEqual(decrypted_products.strip(), decrypt_best_prod.strip())

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
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'В1, В10',
            'Хеш': 'cdd6f7ca257e7f4fc9fa309bce83f7a0c3527b94d576daa29e0f1fac523b6259'}

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_products = prompt_proces_data.decrypting_info_code_best_product(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted='Средства',
        )

        self.assertEqual(decrypted_products.strip(), decrypt_best_one_prod.strip())
