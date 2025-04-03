import ast
import re


def create_dict_from_str(_str: str) -> dict:
    """
    Конвертирует строку в словарь, если позволяет структура.
    Перед этим заменят неправильные кавычки на правильные
    """

    # Заменяем нестандартных кавычек на обычные
    normalized_products = re.sub(r'[«»]', '"', _str)

    return ast.literal_eval(normalized_products)
