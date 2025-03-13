"""В этом модуле тестируем выбор json-схемы"""
# from pprint import pprint
import unittest

from prompt_constructor.json_schemes.main_json_schemes import determine_scheme_by_number_of_products


class TestDetermineSchemeByNumberOfProducts(unittest.TestCase):

    def test_best_product_case(self):
        """
        Тест на выбор схемы для задачи 'Лучшее средство'
        """

        data_for_json = {
            # определяем задачу для выбора в json-схемы
            "Задача": 'Лучшее средство',
            # считаем сколько средств подаем для анализа
            "Количество элементов": 2,
            "Категория": 'Шампуни',
        }

        result = determine_scheme_by_number_of_products(
            data=data_for_json
        )

        # pprint(result)

        # Проверяем, что результат не None и он словарь
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_one_product_case(self):
        """
        Тест на выбор схемы для задачи 'Разбор состава одного средства'
        """

        data_for_json = {
            # определяем задачу для выбора в json-схемы
            "Задача": 'Разбор состава одного средства',
            # считаем сколько средств подаем для анализа
            "Количество элементов": 2,
            "Категория": 'уход за телом',
        }

        expected_result = determine_scheme_by_number_of_products(
            data=data_for_json
        )

        # pprint(expected_result)

        self.assertIsNotNone(expected_result)
        self.assertIsInstance(expected_result, dict)

    def test_unknown_task_case(self):
        """
        Тест на неизвестный код задачи — должен вернуть исключение
        """

        data_for_json = {
            # определяем задачу для выбора в json-схемы
            "Задача": 'Несуществующая задача',
            # считаем сколько средств подаем для анализа
            "Количество элементов": None,
            "Категория": None,
        }

        # Проверяем, что функция выбросит ValueError
        with self.assertRaises(ValueError) as context:
            determine_scheme_by_number_of_products(data=data_for_json)

        # Дополнительно можно проверить сообщение об ошибке
        self.assertEqual(
            str(context.exception),
            "Неизвестный код задачи: 'Несуществующая задача'"
        )
