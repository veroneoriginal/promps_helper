"""В этом модуле тестируем работу пост констурктора"""
import unittest
# pylint: disable=E0611: no-name-in-module
from dev_helpers.data_tools_for_test import ALL_DATA_TOOLS_FOR_TEST
from post_constructor.main_post import get_products_list, create_hashtag

# текущая подборка
BASE_COLLECTION = {
    'Возраст': 32,
    'Группа': 'бесплатная',
    'Задача': 'Лучшее средство',
    'Запрос': 'ЗВ8, ЗВ12',
    'Категория': 'Шампуни',
    'Количество средств': 3,
    'Пол': 'женский',
    'Путь': None,
    'Специалист': 'Т',
    'Средства': None,
    'Тип': 'В1, В10',
    'Хеш': '6ad4852cc0e04bc512762ced9022afec34afbc2c35e129503c1448e4f0b88578',
}

PRODUCTS_SET_1 = {
    'Средства': {
        'Средство_1': ('ALTEREGO ITALY Curego Hydraday', '19000222487'),
        'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
        'Средство_3': ('NATURA SIBERICA Oblepikha', '19000141580'),
    },
}

PRODUCTS_SET_2 = {
    'Набор_1':
        {
            'Средство_1': ('R+CO Dallas Biotin Thickening Shampoo', '24320200017'),
            'Средство_2': ('OUSHEN Curl & shine shampoo', '19000220056'),
        },
    'Набор_2':
        {
            'Средство_1': ('R+CO Atlantis Moisturizing B5 Shampoo', '24320200015'),
            'Средство_2': ('R+CO Television Perfect Hair Conditioner', '24320100036'),
        }
}


class TestPostConstructor(unittest.TestCase):
    """ Тесты пост-конструктора """

    def test_get_products_list(self):
        """
        Тестируем функцию get_products_list
        """

        products = get_products_list(products_dict=PRODUCTS_SET_1)

        self.assertTrue(all((isinstance(elem, tuple) for elem in products)))

    def test_get_products_list_2(self):
        """
        Тестируем функцию get_products_list
        """

        products = get_products_list(products_dict=PRODUCTS_SET_2)

        self.assertTrue(all((isinstance(elem, str) for elem in products)))

    def test_create_hashtag_1(self):
        """
        Тестируем функцию create_hashtag
        """
        BASE_COLLECTION['Средства'] = PRODUCTS_SET_1

        result = create_hashtag(
            data_tools=ALL_DATA_TOOLS_FOR_TEST,
            data=BASE_COLLECTION,
        )

        self.assertEqual(3, result.count('#'))

    def test_create_hashtag_2(self):
        """
        Тестируем функцию create_hashtag
        """
        BASE_COLLECTION['Средства'] = PRODUCTS_SET_2

        result = create_hashtag(
            data_tools=ALL_DATA_TOOLS_FOR_TEST,
            data=BASE_COLLECTION,
        )
        print(result)
        self.assertEqual(2, result.count('#'))
