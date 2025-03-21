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
    best_set_decryped,
    best_set_prompt,
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
            'Категория': 'Уход за кожей лица',
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'PULANNA Bio-gold & Grape'},
            'Тип': 'КЛ1, КЛ2',
            'Хеш': 'a4ece7b3cb7753cfa8d776f0bf751aa8d0ee38b2302c05ac93d4da0bd6c605eb',
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
            task=copy_data_collection['Задача'],
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
            'Категория': 'Шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'OUSHEN Curl & shine shampoo',
                         'Средство_2': 'NATURA SIBERICA Oblepikha',
                         'Средство_3': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'В1, В10',
            'Хеш': '6fa98fcf493402f8874e2771f891b25e8e5abbd8f8b6c4555e014791f3581407'}

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
            task=copy_data_collection['Задача'],
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
            'Категория': 'Шампуни',
            'Количество средств': 3,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'R+CO Television Perfect Hair Conditioner',
                         'Средство_2': 'R+CO Atlantis Moisturizing B5 Conditioner',
                         'Средство_3': 'R+CO TELEVISION Perfect Hair Masque'},
            'Тип': 'В1, В10',
            'Хеш': '6a161403f3463652963265593cd6faf0ce327b9ef49d0fc183ee340fbbe9dc39',
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
            task=copy_data_collection['Задача'],
        )

        self.assertEqual(prompt, best_combination_prompt)

    def test_main_decryp_data_from_best_set(self):
        """
        Проверка, что данные текущей подборки по коду 'Лучшая пара'
        расшифровываются и что промпт получается корректный
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
            'Средства': {'Пара_1': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                                    'Средство_2': 'ALTEREGO ITALY Curego Hydraday'},
                         'Пара_2': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                                    'Средство_2': 'ALTEREGO ITALY Curego Hydraday'}},
            'Тип': 'В1, В10',
            'Хеш': '1961938df56f42e4cd8a467ad1b87ab1b556f9bc3f022fb6a1a8919889cd5292',
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
        self.assertEqual(decrypted_collection, best_set_decryped)

        prompt_constructor = PromptConstructor()

        # проверяем результат создания промпта по текущей подборке
        prompt = prompt_constructor.main_constructor_prompt(
            data_decrypted=decrypted_collection,
            task=copy_data_collection['Задача'],
        )

        self.assertEqual(prompt, best_set_prompt)
