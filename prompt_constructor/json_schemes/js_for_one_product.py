def create_base_json_scheme_for_one_product() -> dict:
    """
    Функция, внутри которой создается базовая конструкция универсальной
    json-схемы для анализа одного средства, которая используется во всех категориях
    """
    schema = {
        "name": "cosmetic_product_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Название средства"
                        },
                        "main_components": {
                            "type": "string",
                            "description": "Подробно поясни суть основных компонентов"
                        },
                        "active_ingredients": {
                            "type": "string",
                            "description": "Подробно поясни суть активных компонентов"
                        },
                        "moisturizing_and_care": {
                            "type": "string",
                            "description":
                                "Подробно поясни суть увлажняющих и ухаживающих компонентов"
                        },
                        "preservatives_and_ph_regulators": {
                            "type": "string",
                            "description":
                                "Подробно поясни суть консервантов и регуляторов pH, если они есть"
                        },
                        "banned_or_unwanted": {
                            "type": "string",
                            "description":
                                "Подробно поясни суть запрещенных или нежелательных компонентов"
                        },
                        "additional_properties": {
                            "type": "string",
                            "description":
                                "Если есть какие-то дополнительные свойства, укажи их и поясни"
                        },
                        "texture": {
                            "type": "string",
                            "description": "Текстура"
                        },
                        "plus": {
                            "type": "string",
                            "description": "Плюсы средства"
                        },
                        "minus": {
                            "type": "string",
                            "description": "Минусы средства"
                        },
                        "conclusion": {
                            "type": "string",
                            "description": "Вывод, исходя из всей вышепредставленной информации"
                        }
                    },
                    "required": [
                        "title",
                        "main_components",
                        "active_ingredients",
                        "moisturizing_and_care",
                        "preservatives_and_ph_regulators",
                        "banned_or_unwanted",
                        "additional_properties",
                        "texture",
                        "plus",
                        "minus",
                        "conclusion"
                    ],
                    "additionalProperties": False
                }
            },
            "required": ["product"],
            "additionalProperties": False
        }
    }

    return schema


# словарь для дополнения основной схемы
CATEGORY_EXTENSIONS = {

    "уход за телом":
        {
            "properties": {
                "skin_type_impact":
                    {"type": "string",
                     "description": "Влияние на тип кожи (увлажнение, смягчение)"},
                "exfoliation_intensity":
                    {"type": "string",
                     "description": "Интенсивность пилинга (для скрабов)"},
                "protection_duration":
                    {"type": "string",
                     "description": "Длительность защиты (для дезодорантов)"},
                "foaming_effect":
                    {"type": "string",
                     "description": "Пенообразование (для гелей)"}
            },
            "required":
                [
                    "skin_type_impact",
                    "exfoliation_intensity",
                    "protection_duration",
                    "foaming_effect",
                ],
        },

    "уход за кожей лица": {
        "properties": {
            "skin_type_impact":
                {"type": "string",
                 "description": "Влияние на тип кожи (комедогенность, увлажнение)"},
            "spf_level":
                {"type": "string",
                 "description": "Уровень SPF (если есть)"},
            "application_time":
                {"type": "string",
                 "description": "Время нанесения (если требуется выдержка)"},
            "ph_level":
                {"type": "string",
                 "description": "Уровень pH"},
            "exfoliation_intensity":
                {"type": "string",
                 "description": "Интенсивность пилинга (для скрабов)"},
            "eye_area_effect":
                {"type": "string",
                 "description": "Эффект на область глаз (для патчей)"},
        },
        "required":
            [
                "skin_type_impact",
                "spf_level",
                "application_time",
                "ph_level",
                "exfoliation_intensity",
                "eye_area_effect",
            ]
    },
    "макияж": {
        "properties": {
            "durability":
                {"type": "string",
                 "description": "Стойкость"},
            "finish":
                {"type": "string",
                 "description": "Финиш (матовый, сияющий)"},
            "pigmentation":
                {"type": "string",
                 "description": "Пигментация"},
            "coverage":
                {"type": "string",
                 "description": "Покрытие (лёгкое, среднее, плотное)"},
            "water_resistance":
                {"type": "boolean",
                 "description": "Водостойкость"},
            "spf_level":
                {"type": "number",
                 "description": "Уровень SPF"},
        },
        "required":
            [
                "durability",
                "finish",
                "pigmentation",
                "coverage",
                "water_resistance",
                "spf_level",
            ]
    },
    "стайлинг волос": {
        "properties": {
            "fixation_level":
                {
                    "type": "string",
                    "description": "Степень фиксации",
                },
            "hair_feel":
                {
                    "type": "string",
                    "description": "Ощущение на волосах (утяжеляет/не утяжеляет) и общий эффект",
                }
        },
        "required": [
            "fixation_level",
            "hair_feel",
        ]
    },
    "парфюмерия": {
        "properties": {
            "main_notes":
                {
                    "type": "string",
                    "description": "Основные ноты",
                },
            "durability":
                {
                    "type": "string",
                    "description": "Стойкость",
                },
            "scent_evolution":
                {
                    "type": "string",
                    "description": "Раскрытие аромата",
                }
        },
        "required": [
            "main_notes",
            "durability",
            "scent_evolution",
        ]
    },

}


def create_json_scheme_for_one_product(
        data: dict,
) -> dict:
    """
    Функция для формирования json-схемы для кода задачи 'Разбор состава одного средства'

    :param data: словарь с информацией для выбора json-схемы из которого для этой функции берется
    значение по ключу 'Категория'
    :return: json-схема для заданного количества средств
    """

    # Получаем базовую схему
    schema = create_base_json_scheme_for_one_product()

    # Проверяем, есть ли для категории расширения
    if data["Категория"] in CATEGORY_EXTENSIONS:
        extension = CATEGORY_EXTENSIONS[data["Категория"]]
        # Добавляем новые свойства
        schema["schema"]["properties"]["product"]["properties"].update(extension["properties"])
        # Добавляем новые обязательные поля
        schema["schema"]["properties"]["product"]["required"].extend(extension["required"])

    return schema
