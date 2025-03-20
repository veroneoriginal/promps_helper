"""
В этом модуле тестируем создание промпта
"""
import copy

import unittest
# from pprint import pprint

from prompt_constructor.prompt_constructor import PromptConstructor
from prompt_constructor.prompt_processing_data import PromptProcessingData

from prompt_constructor.test_constructor.data_tools import data_tools

from prompt_constructor.test_constructor.constants import (
    decrypted_collection_one_product,
    prompt_for_one_product,
    decrypted_collection_carcinogen_free,
    expected_prompt_for_best_prod_carcinogen,
    best_combination_decryped,
    best_combination_prompt,
)


class TestPromptConstructor(unittest.TestCase):
    """
    Тесты на get_prompt / PromptConstructor
    """

    def test_main_one_product(self):
        """
        Проверка, что данные текущей подборки по коду
        'Разбор состава одного средства' расшифровываются и
        что промпт получается корректный
        """

        # текущая подборка
        data_collection = {
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

        # создание копии словаря с текущей подборкой,
        # т.к. иначе не добраться до кода задачи
        copy_data_collection = copy.deepcopy(data_collection)

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_collection = prompt_proces_data.main_decryp_data_from_current_collection(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # проверяем результат расшифровки по текущей подборке
        self.assertEqual(decrypted_collection, decrypted_collection_one_product)

        prompt_constructor = PromptConstructor()

        # проверяем результат создания промпта по текущей подборке
        prompt = prompt_constructor.main_constructor_prompt(
            data_decrypted=decrypted_collection,
            data_collection=copy_data_collection,
        )

        self.assertEqual(prompt, prompt_for_one_product)

    def test_main_decryp_data_from_current_collection_carcinogen(self):
        """
        Проверка, что данные текущей подборки по коду
        'Лучшее средство без канцерогенов' расшифровываются и
        что промпт получается корректный
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

        # создание копии словаря с текущей подборкой,
        # т.к. иначе не добраться до кода задачи
        copy_data_collection = copy.deepcopy(data_collection)

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_collection = prompt_proces_data.main_decryp_data_from_current_collection(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # проверяем результат расшифровки по текущей подборке
        self.assertEqual(decrypted_collection, decrypted_collection_carcinogen_free)

        prompt_constructor = PromptConstructor()

        # проверяем результат создания промпта по текущей подборке
        prompt = prompt_constructor.main_constructor_prompt(
            data_decrypted=decrypted_collection,
            data_collection=copy_data_collection,
        )

        self.assertEqual(prompt, expected_prompt_for_best_prod_carcinogen)

    def test_main_decryp_data_from_best_combination(self):
        """
        Проверка, что данные текущей подборки по коду 'Лучшее сочетание'
        расшифровываются и что промпт получается корректный
        """

        # текущая подборка
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее сочетание',
            'Запрос': 'ЗВ8, ЗВ12',
            'Исходное средство': 'R+CO Atlantis Moisturizing B5 Shampoo',
            'Итог': None,
            'Категория': 'шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'R+CO Television Perfect Hair Conditioner',
                         'Средство_2': 'R+CO Atlantis Moisturizing B5 Conditioner',
                         'Средство_3': 'R+CO TELEVISION Perfect Hair Masque'},
            'Тип': 'В1, В10',
            'Хеш': '2d2918a9e091164a303dd3c652d052b2b2bcc3bb88dd7c075a4c8b31aed75b6d',
        }

        # создание копии словаря с текущей подборкой,
        # т.к. иначе не добраться до кода задачи
        copy_data_collection = copy.deepcopy(data_collection)

        prompt_proces_data = PromptProcessingData(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # текущая подборка (расшифрованная)
        decrypted_collection = prompt_proces_data.main_decryp_data_from_current_collection(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        # проверяем результат расшифровки по текущей подборке
        self.assertEqual(decrypted_collection, best_combination_decryped)

        prompt_constructor = PromptConstructor()

        # проверяем результат создания промпта по текущей подборке
        prompt = prompt_constructor.main_constructor_prompt(
            data_decrypted=decrypted_collection,
            data_collection=copy_data_collection,
        )

        self.assertEqual(prompt, best_combination_prompt)
