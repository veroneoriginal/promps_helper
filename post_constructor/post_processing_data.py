from collections import defaultdict


def build_description(
        code_string: str,
        section_data: dict,
        detailed: bool = False
) -> str:
    """
    Универсальная функция для сборки текста из кодов.
    :param code_string: строка с кодами (напр. "В1, В2")
    :param section_data: словарь с данными (Тип или Запрос)
    :param detailed: True — для подробной версии, False — для короткой
    :return: строка с описанием
    """
    items = [i.strip() for i in code_string.strip().split(",")]
    grouped = defaultdict(list)
    for code in items:
        if code in section_data:
            block = section_data[code]
            key = block["Область применения"]
            if detailed:
                grouped[key].append(f'\n- **{block["Суть"].lower()}** ({block["Описание"]})')
            else:
                grouped[key].append(f' {block["Суть"].lower()}')
    # Сборка финального текста
    result_lines = []
    for key, values in grouped.items():
        smile = get_smile_for_key(key)
        line = f"**{smile} {key}:**" + ",".join(values)
        result_lines.append(line)

    return "\n".join(result_lines)


def get_smile_for_key(key: str) -> str:
    """
    Возвращает смайлик для категории
    """

    SMILES = {
        # Пол
        'мужской': '🧑',
        'женский': '👩',
        # Запрос
        'волосы': '🙆',
        'кожа головы': '💆',
        'кожа лица': '🥽',
        # Тип
        'тип волос': '🙆',
        'тип кожи головы': '💆',
        'тип кожи лица': '🥽',
    }

    return SMILES.get(key.lower(), '🔹')
