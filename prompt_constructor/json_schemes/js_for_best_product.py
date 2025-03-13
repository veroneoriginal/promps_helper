def create_json_scheme_for_best_product(
        product_count: int,
) -> dict:
    """
    Функция для динамического формирования json-схемы для кода задачи 'Лучшее средство'

    :param product_count: количество средств, которые анализируются
    :return: json-схема для заданного количества средств
    """
    schema = {
        "name": "cosmetics_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "best_product": {
                    "type": "string",
                    "description": "Лучшее средство"
                },
                "result": {
                    "type": "string",
                    "description": "Итоговая рекомендация, вывод"
                }
            },
            "required": ["best_product", "result"],
            "additionalProperties": False
        }
    }

    # Добавляем продукты динамически
    products = {}
    for i in range(1, product_count + 1):
        product_key = f"product_{i}"
        products[product_key] = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": f"Название {i}-го средства"
                },
                "plus": {
                    "type": "string",
                    "description": f"Описание плюсов {i}-го средства (без названия средства)"
                },
                "minus": {
                    "type": "string",
                    "description": f"Описание минусов {i}-го средства (без названия средства)"
                },
                "best_product": {
                    "type": "boolean",
                    "description": "Если это средство стало лучшим, поставь здесь True,"
                                   " если нет, то False"
                }
            },
            "required": ["title", "plus", "minus", "best_product"],
            "additionalProperties": False
        }

    # Добавляем продукты в свойства схемы
    schema["schema"]["properties"].update(products)

    # Добавляем продукты в список `required`
    schema["schema"]["required"].extend(products.keys())

    return schema
