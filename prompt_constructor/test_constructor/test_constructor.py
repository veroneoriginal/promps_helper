"""
В этом модуле тестируем создание промпта
"""
import copy

import unittest
from prompt_constructor.prompt_constructor import PromptConstructor
from prompt_constructor.prompt_processing_data import PromptProcessingData

from prompt_constructor.test_constructor.constants import (
    data_tools,
    decrypted_collection_one_product,
    prompt_for_one_product,
)


class TestPromptConstructor(unittest.TestCase):
    """
    Тесты на get_prompt / PromptConstructor
    """

    def test_main_decryp_data_from_current_collection(self):
        """
        Проверка, что данные текущей подборки расшифровываются
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
