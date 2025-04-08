import ast
import re


def create_dict_from_str(_str: str) -> dict:
    """
    Конвертирует строку в словарь, если позволяет структура.
    Перед этим заменят неправильные кавычки на правильные
    """
    if not isinstance(_str, str):
        raise ValueError(f"Ожидалась строка, но получено: {type(_str)} -> {_str}")
    # Заменяем нестандартных кавычек на обычные
    normalized_products = re.sub(r'[«»]', '"', _str)
    return ast.literal_eval(normalized_products)


def is_collection_without_user_parameters(collection_data: dict):
    """
    Возвращает True, если подборка БЕЗ учёта параметров пользователя
    :param collection_data: данные подборки
    """

    return collection_data['Параметры'].lower().strip() == 'не учитывать'
