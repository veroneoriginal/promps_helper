from prompt_constructor.json_schemes.js_for_best_product import create_json_scheme_for_best_product
from prompt_constructor.json_schemes.js_for_one_product import create_json_scheme_for_one_product


def determine_scheme_by_number_of_products(
        code_task: str,
        category: str | None,
        product_count: int | None,
) -> dict | None:
    """
    Функция для определения json-схемы для отправки запроса

    :param code_task: код задачи для выбора json-схемы
    :param category: категория средства для выбора подходящей схемы
    :param product_count: количество средств, которые анализируюся
    :return: json-scheme на заданное количество продуктов
    """
    scheme = {
        'Лучшее средство': create_json_scheme_for_best_product(product_count),
        'Разбор состава одного средства': create_json_scheme_for_one_product(category),
    }

    try:
        return scheme[code_task]
    except KeyError as exc:
        raise ValueError(f"Неизвестный код задачи: '{code_task}'") from exc
