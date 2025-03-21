import unittest
import json
from excel_process_data.utils.utils import counting_hash

best_product = ''


class TestUtils(unittest.TestCase):

    def test_counting_hash_best_set(self):
        """
        Тест для проверки функции counting_hash для вложенной структуры, например,
        код 'Лучший набор'
        """

        best_set = {
            'Возраст': 32,
            'Задача': 'Лучший набор',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Категория': 'Шампуни',
            'Лучший вариант': None,
            'Пол': 'женский',
            'Специалист': 'Т',
            'Средства': json.dumps(
                {
                    'Пара_1': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                               'Средство_2': 'ALTEREGO ITALY Curego Hydraday'},
                    'Пара_2': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                               'Средство_2': 'ALTEREGO ITALY Curego Hydraday'},
                }
            ),
            'Тип': 'В1, В10',
            'Хеш': '1961938df56f42e4cd8a467ad1b87ab1b556f9bc3f022fb6a1a8919889cd5292',
        }
        expected_hash = best_set['Хеш']

        result_hash = counting_hash(data=best_set)

        # Проверяем, что результат совпадает с ожидаемым значением
        self.assertEqual(result_hash, expected_hash, 'Хеши не равны')

    def test_counting_hash_best_product(self):
        """
        Тест для проверки функции counting_hash БЕЗ вложенной структуры, например,
        код 'Лучшее средство'
        """

        best_products = {
            'Категория': 'Шампуни',
            'Пол': 'женский',
            'Возраст': 32,
            'Тип': 'В1, В10',
            'Запрос': 'ЗВ8, ЗВ12',
            'Задача': 'Лучшее средство',
            'Специалист': 'Т',
            'Средства':
                '{\n«Средство_1» : «ALTEREGO ITALY Curego Hydraday»,\n'
                '«Средство_2» : «OUSHEN Curl & shine shampoo»,\n'
                '«Средство_3» : «NATURA SIBERICA Oblepikha»\n}',
            'Лучший вариант': None,
            'Итог': None,
            'Хеш': '9fc07df0fc52279925506b22111b9c7e7672184318fb2259d2e5e28220a682e3'}
        expected_hash = best_products['Хеш']

        result_hash = counting_hash(data=best_products)

        # Проверяем, что результат совпадает с ожидаемым значением
        self.assertEqual(result_hash, expected_hash, 'Хеши не равны')
