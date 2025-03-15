from prompt_constructor.json_schemes.js_for_best_product import create_json_scheme_for_best_product
from prompt_constructor.json_schemes.js_for_one_product import create_json_scheme_for_one_product


def determine_scheme_by_number_of_products(
        data: dict,
        product_categories: dict,
) -> dict | None:
    """
    Функция для определения json-схемы для отправки запроса

    :param data: словарь с информацией для выбора json-схемы
    :param product_categories: словарь со всеми параметрами для разных категорий продуктов
    :return: json-scheme на заданное количество продуктов
    """
    scheme = {
        'Лучшее средство': create_json_scheme_for_best_product,
        'Лучшее средство без канцерогенов': create_json_scheme_for_best_product,
        'Разбор состава одного средства': create_json_scheme_for_one_product,
    }

    task = data["Задача"]

    if task == 'Разбор состава одного средства':
        return scheme[task](data=data, product_categories=product_categories)

    return scheme[task](data)
