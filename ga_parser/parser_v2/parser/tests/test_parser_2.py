import unittest
from typing import AnyStr

from bs4 import BeautifulSoup

from ga_parser.parser_v2.parser.generation_product_data import (
    get_item_title_description,
    get_characteristics,
    get_application_instruction,
    get_compound,
    get_brand,
    get_price_in_stock,
    get_measure,
    get_img_link,
    get_additional_info,
)


def load_test_html(file_name: str) -> AnyStr:
    with open(f'ga_parser/html_for_tests/{file_name}', 'r', encoding='utf-8') as file:
        return file.read()


html = load_test_html(file_name='html_test_1.html')


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.soup = BeautifulSoup(html, 'html.parser')

    def test_get_item_title_description(self):
        """
        Для получения:  Артикул, Название, Описание
        """
        result = get_item_title_description(soup=self.soup)
        print('test_get_item_title_description:')
        print(result)

    def test_get_characteristics(self):
        """
        Для получения: Тип продукта, Для кого, Назначение, Тип волос,
        Тип кожи, Область применения, Текстура, Финиш, Объём
        """
        result = get_characteristics(soup=self.soup)
        print('test_get_characteristics:')
        print(result)

    def test_get_application_instruction(self):
        """
        Для получения:  Применение
        """
        result = get_application_instruction(soup=self.soup)
        print('test_get_application_instruction:')
        print(result)

    def test_get_compound(self):
        """
        Для получения:  Cостав
        """
        result = get_compound(soup=self.soup)
        print('test_get_compound:')
        print(result)

    def test_get_brand(self):
        """
        Для получения:  Бренд, Страна бренда, Описание бренда
        """
        result = get_brand(soup=self.soup)
        print('test_get_brand:')
        print(result)

    def test_get_price_in_stock(self):
        """
        Для получения:  Цена без скидки
        """
        result = get_price_in_stock(soup=self.soup)
        print('test_get_price_in_stock:')
        print(result)

    def test_get_measure(self):
        """
        Для получения:  Мера, Юниты меры
        """
        characteristics = get_characteristics(soup=self.soup)
        result = get_measure(characteristics=characteristics)
        print('test_get_measure:')
        print(result)

    def test_get_img_link(self):
        """
        Для получения:  Ссылка на изображение
        """
        result = get_img_link(soup=self.soup)
        print('test_get_img_link:')
        print(result)

    def test_get_additional_info(self):
        """
        Для получения:  Дополнительная информация
        """
        result = get_additional_info(soup=self.soup)
        print('test_get_additional_info:')
        print(result)
