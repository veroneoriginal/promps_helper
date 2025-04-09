import ast
import re
import traceback


def create_dict_from_str(
        _str: str,
        row_number: int,
) -> dict | None:
    """
    Конвертирует строку в словарь, если позволяет структура.
    Перед этим заменят неправильные кавычки на правильные

    :param _str: строка со средствами для преобразования
    :param row_number: номер строки с подборкой
    """
    if not isinstance(_str, str):
        raise ValueError(
            f"⚠ Подборка в строке № {row_number}: ошибка при конвертации "
            f"с средствами в словарь - "
            f"ожидалась строка, но получено: {type(_str)} -> {_str}"
        )
    try:
        # Заменяем кавычки «» на стандартные "
        normalized = _str.replace('«', '"').replace('»', '"')

        # Заменяем круглые скобки на кортежный формат с квадратными (для ast.literal_eval)
        normalized = re.sub(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', r'("\1", "\2")', normalized)
        return ast.literal_eval(normalized)
    except Exception as exc:
        print(
            f"⚠ Подборка в строке № {row_number}: ошибка при конвертации "
            f"с средствами в словарь - {exc}\n"
            f"{traceback.format_exc()}"
        )
        raise


def is_collection_without_user_parameters(collection_data: dict):
    """
    Возвращает True, если подборка БЕЗ учёта параметров пользователя
    :param collection_data: данные подборки
    """

    return collection_data['Параметры'].lower().strip() == 'не учитывать'
