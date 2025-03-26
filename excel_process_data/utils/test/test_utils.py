import unittest
from excel_process_data.utils.utils import counting_hash


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
            'Категория': 'Шампуни',
            'Пол': 'женский',
            'Путь': None,
            'Специалист': 'Т',
            'Средства': '{\n'
                        '«Набор_1» : \n'
                        '{\n'
                        '«Средство_1» : («R+CO Dallas Biotin Thickening Shampoo»,  «24320200017»),\n'
                        '«Средство_2» : («R+CO TELEVISION Perfect Hair Masque»,  «19760310342»)\n'
                        '},\n'
                        '«Набор_2» : \n'
                        '{\n'
                        '«Средство_1» : («R+CO Atlantis Moisturizing B5 Shampoo», «24320200015»),\n'
                        '«Средство_2» : («R+CO Television Perfect Hair Conditioner», «24320100036»)\n'
                        '},\n'
                        '}',
            'Тип': 'В1, В10',
            'Хеш': 'de5353e9f505c2234028fd6fe6510f7f81e2ef13dd7d1dd6351887387219b832'
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
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Категория': 'Шампуни',
            'Пол': 'женский',
            'Путь': None,
            'Специалист': 'Т',
            'Средства': '{\n'
                        '«Средство_1» : («ALTEREGO ITALY Curego Hydraday», «19000222487»),\n'
                        '«Средство_2» : («OUSHEN Curl & shine shampoo», «19000220056»),\n'
                        '«Средство_3» : («NATURA SIBERICA Oblepikha», «19000141580»),\n'
                        '«Средство_4» : («WELEDA Millet Nourishing»,«15180100004»),\n'
                        '«Средство_5» : («PAYOT Shampoing doux biome-friendly», «19000153618»),\n'
                        '«Средство_6» : («LADOR Keratin LPP», «19760200012»)\n'
                        '}',
            'Тип': 'В1, В10',
            'Хеш': 'bae5152f3170fdc223884058b8e99fad22e4574b9dc71fd4fc544522f5401728',
        }
        expected_hash = best_products['Хеш']

        result_hash = counting_hash(data=best_products)

        # Проверяем, что результат совпадает с ожидаемым значением
        self.assertEqual(result_hash, expected_hash, 'Хеши не равны')
