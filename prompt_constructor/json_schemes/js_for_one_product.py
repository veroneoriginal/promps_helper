"""
В этом модуле собраны функции для формирования json-схемы для кода 'Разбор состава одного средства'
"""

def format_properties(
        properties_dict: dict,
) -> dict:
    """
    Преобразует словарь свойств в формат JSON-схемы.

    :param properties_dict: словарь полей с типом и описанием
    :return: словарь с блоками "properties" и "required"
    """
    formatted = {
        "properties": {},
        "required": []
    }

    for key, (prop_type, description) in properties_dict.items():
        formatted["properties"][key] = {
            "type": prop_type,
            "description": description
        }
        formatted["required"].append(key)

    return formatted


def create_base_json_scheme_for_one_product(
        properties_dict: dict,
) -> dict:
    """
    Функция, внутри которой создается базовая конструкция универсальной
    json-схемы для анализа одного средства, которая используется во всех категориях

    :param properties_dict: словарь с настройками дляформирования json-схемы
    :return: словарь в виде готовой json-схемы
    """

    product_schema = format_properties(properties_dict)

    schema = {
        "name": "cosmetic_product_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": product_schema["properties"],
                    "required": product_schema["required"],
                    "additionalProperties": False
                }
            },
            "required": ["product"],
            "additionalProperties": False
        }
    }

    return schema


def create_json_scheme_for_one_product(
        data: dict,
        product_categories: dict,
) -> dict:
    """
    Функция для формирования json-схемы для кода задачи 'Разбор состава одного средства'

    :param data: словарь с информацией для выбора json-схемы из которого для этой функции берется
    значение по ключу 'Категория'
    :param product_categories: словарь со всеми параметрами для разных категорий продуктов
    :return: json-схема для заданного количества средств
    """

    # Получаем базовую схему
    schema = create_base_json_scheme_for_one_product(product_categories["Базовые настройки"])

    category = data.get("Категория")

    if category in product_categories:
        extension_properties = product_categories[category]
        extension_schema = format_properties(extension_properties)

        # Добавляем новые поля в schema
        product_properties = schema["schema"]["properties"]["product"]["properties"]
        product_required = schema["schema"]["properties"]["product"]["required"]

        product_properties.update(extension_schema["properties"])
        product_required.extend(extension_schema["required"])

    return schema
