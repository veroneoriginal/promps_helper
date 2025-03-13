"""В этом модуле тестируем выбор json-схемы"""
# from pprint import pprint
import unittest

from prompt_constructor.json_schemes.main_json_schemes import determine_scheme_by_number_of_products


class TestDetermineSchemeByNumberOfProducts(unittest.TestCase):

    def test_best_product_case(self):
        """
        Тест на выбор схемы для задачи 'Лучшее средство'
        """
        code_task = 'Лучшее средство'
        product_count=2

        result = determine_scheme_by_number_of_products(
            code_task=code_task,
            category=None,
            product_count=product_count
        )

        # pprint(result)

        # Проверяем, что результат не None и он словарь
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)


    def test_one_product_case(self):
        """
        Тест на выбор схемы для задачи 'Разбор состава одного средства'
        """
        code_task = 'Разбор состава одного средства'
        category='уход за телом'

        expected_result = determine_scheme_by_number_of_products(
            code_task=code_task,
            category=category,
            product_count=None
        )

        # pprint(expected_result)

        self.assertIsNotNone(expected_result)
        self.assertIsInstance(expected_result, dict)


    def test_unknown_task_case(self):
        """
        Тест на неизвестный код задачи — должен вернуть None
        """
        code_task = 'Несуществующая задача'

        result = determine_scheme_by_number_of_products(
            code_task=code_task,
            category=None,
            product_count=None
        )

        # pprint(result)

        self.assertIsNone(result)
