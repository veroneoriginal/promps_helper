"""В этом модуле тестируем работу пост констурктора"""

from post_constructor.main_post import get_products_list
from post_constructor.test.data_tools import data_tools

# текущая подборка
data_collection = {
    'Возраст': 32,
    'Группа': 'бесплатная',
    'Задача': 'Лучшее средство',
    'Запрос': 'ЗВ8, ЗВ12',
    'Категория': 'Шампуни',
    'Количество средств': 3,
    'Пол': 'женский',
    'Путь': None,
    'Специалист': 'Т',
    'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                 'Средство_2': 'OUSHEN Curl & shine shampoo',
                 'Средство_3': 'NATURA SIBERICA Oblepikha'},
    'Тип': 'В1, В10',
    'Хеш': '6ad4852cc0e04bc512762ced9022afec34afbc2c35e129503c1448e4f0b88578',
}

# ответ от gpt
path_to_result_recommend = '00_base/00_info_for_post/27_03_25/1_Шампуни_бесплатная/00_source/02_answer_gpt'

# куда сохранять
path_for_save = '00_base/00_info_for_post/27_03_25/1_Шампуни_бесплатная/00_source/05_text'


def test_create_hashtag():
    """
    Тестируем функцию create_hashtag
    """
    # 1. Получаем список средств из текущей подборки и проверяем, что это список
    products = get_products_list(data_collection['Средства'])
    assert isinstance(products, list), "products должен быть списком"

    # 2. Ожидаем получить такой список
    expected_list = ['ALTEREGO ITALY Curego Hydraday',
                     'OUSHEN Curl & shine shampoo',
                     'NATURA SIBERICA Oblepikha']

    assert products == expected_list, f"Ожидалось {expected_list}, но получили {products}"

    # 3. Проверяем, что будет содержаться в переменной brand

    # 3.1 первая часть запроса - словарь, не пустой
    for product in products:
        brand = data_tools.get('Средства', {})
        assert isinstance(brand, dict), "brand должен быть словарём"
        assert brand, "brand не должен быть пустым"

    # 3.2 вторая часть запроса - тоже словарь, не пустой
    for product in products:
        brand = data_tools.get('Средства', {}).get(product, {})
        assert isinstance(brand, dict), "brand должен быть словарём"
        assert brand, "brand не должен быть пустым"

    # 3.3 третья часть запроса - тоже словарь, не пустой
    # если в таблице в ячейке бренда пусто, то когда мы забираем словарь параметр 'Бренд': None
    for product in products:
        brand = data_tools.get('Средства', {}).get(product, {}).get('Бренд')
        if brand is None:
            assert brand is None, f"Ожидался brand == None, но получили: {brand}"
