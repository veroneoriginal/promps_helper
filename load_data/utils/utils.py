def extract_text(
        data: dict,
        main_key: str,
        description_key: str = "Описание",
) -> str:
    """  Функция для извлечения нужных данных и объединения их в строку"""

    # Проверка, что data - это словарь
    if isinstance(data, dict):
        return f"{data.get(main_key, '')}. {data.get(description_key, '')}".strip()
    # Если вдруг data - не словарь, просто возвращаем как строку
    return str(data)
