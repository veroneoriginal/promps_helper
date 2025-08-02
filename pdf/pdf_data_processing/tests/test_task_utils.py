# pylint: disable=C0301 line-too-long
# pylint: disable=E0611 no-name-in-module
import unittest

from pdf.pdf_data_processing.tasks_utils import (
    calculate_price_per_standard_unit,
    calc_base_price_ratio,
)
from dev_helpers.data_tools_for_test import ALL_DATA_TOOLS_FOR_TEST


class TestTasksUtils(unittest.TestCase):
    """ Тесты вспомогательных функций для разных задач """

    def test_calculate_price_per_standard_unit(self):
        """
        Расчёт цены за стандартное количество
        """

        data_samples = [
            {"Мера": "объем", "Количество меры": 300, "Юниты меры": "мл", "Стоимость руб": 30_000},
            {"Мера": "объем", "Количество меры": 80, "Юниты меры": "мл", "Стоимость руб": 8000},
            {"Мера": "объем", "Количество меры": 50, "Юниты меры": "гр", "Стоимость руб": 500},
            {"Мера": "объем", "Количество меры": 700, "Юниты меры": "гр", "Стоимость руб": 777},
            {"Мера": "объем", "Количество меры": 30, "Юниты меры": "гр", "Стоимость руб": 300},
            {"Мера": "объем", "Количество меры": 2, "Юниты меры": "л", "Стоимость руб": 2900},
            {"Мера": "объем", "Количество меры": 2, "Юниты меры": "кг", "Стоимость руб": 4000},
        ]

        expected_result = [
            '100 мл / 10000 р.',
            '50 мл / 5000 р.',
            '50 гр / 500 р.',
            '100 гр / 111 р.',
            '50 гр / 500 р.',
            '100 мл / 145 р.',
            '100 гр / 200 р.',

        ]

        res_list = []
        for data in data_samples:
            result = calculate_price_per_standard_unit(
                quantity=data["Количество меры"],
                unit=data["Юниты меры"],
                price_rub=data["Стоимость руб"]
            )
            res_list.append(result)

        self.assertEqual(expected_result, res_list)

    def test_best_product_calc_base_price_ratio(self):
        """
        Готовит строку 'Количество мера / цена'
        Например: '190 мл / 1612 р.'
        """
        result = calc_base_price_ratio(product=ALL_DATA_TOOLS_FOR_TEST['ALTEREGO ITALY Scalpego Balancing']['19000222491'])
        self.assertEqual('300 мл / 3500 рублей', result)
