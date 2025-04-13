import re
import traceback


def parse_collection_products_data(raw: str) -> dict:
    """
    Парсит средства подборки из строки
    :param raw: строка с средствами
    :return: словарь с средствами и артикулами
    """
    result = {}
    current_group = None
    raw = raw.strip().replace("«", "\"").replace("»", "\"")

    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    group_header_pattern = re.compile(r'^(Набор_\d+)\s*:?\s*$')
    entry_pattern = re.compile(r'^(Средство_\d+)\s*:\s*(.+?),\s*(\d+)$')

    for line in lines:
        group_match = group_header_pattern.match(line)
        entry_match = entry_pattern.match(line)

        if group_match:
            current_group = group_match.group(1)
            result[current_group] = {}
        elif entry_match:
            key, name, code = entry_match.groups()
            item = (name.strip(), code.strip())
            if current_group:
                result[current_group][key] = item
            else:
                result[key] = item
        else:
            message = f"⚠️ Не смог спарсить средство из подборки: {line}"
            print(message)
            raise ValueError(message)

    return result

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
        return parse_collection_products_data(_str)
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
