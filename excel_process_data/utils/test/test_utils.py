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
                        '«Средство_1» : «R+CO Dallas Biotin Thickening Shampoo»,\n'
                        '«Средство_2» : «R+CO TELEVISION Perfect Hair Masque»\n'
                        '},\n'
                        '«Набор_2» : \n'
                        '{\n'
                        '«Средство_1» : «R+CO Atlantis Moisturizing B5 Shampoo»,\n'
                        '«Средство_2» : «R+CO Television Perfect Hair Conditioner»\n'
                        '},\n'
                        '}',
            'Тип': 'В1, В10',
            'Хеш': 'cfc392bfd045eb548d8989bb96c1ac57385a16a804291d38f93415ac1ae340d1'
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
                        '«Средство_1» : «ALTEREGO ITALY Curego Hydraday»,\n'
                        '«Средство_2» : «OUSHEN Curl & shine shampoo»,\n'
                        '«Средство_3» : «NATURA SIBERICA Oblepikha»,\n'
                        '«Средство_4» : «WELEDA Millet Nourishing»,\n'
                        '«Средство_5» : «PAYOT Shampoing doux biome-friendly»,\n'
                        '«Средство_6» : «LADOR Keratin LPP»\n'
                        '}',
            'Тип': 'В1, В10',
            'Хеш': '77be47509a12d0b36ec98f0097eaf7d89dbe01a88d502baf567cdd0eacee74c3',
        }
        expected_hash = best_products['Хеш']

        result_hash = counting_hash(data=best_products)

        # Проверяем, что результат совпадает с ожидаемым значением
        self.assertEqual(result_hash, expected_hash, 'Хеши не равны')
