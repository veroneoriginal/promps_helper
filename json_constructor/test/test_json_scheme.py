# pylint: skip-file
"""
В этом модуле тестируем выбор json-схемы
"""

import unittest
# from pprint import pprint

from json_constructor.json_creator import JsonCreator
from json_constructor.json_processing_data import JsonProcessingData
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES


class TestJsonScheme(unittest.TestCase):

    def test_decryption_task_best_product(self):
        """
        Проверка работы метода decryption_task_best_product для преобразования словаря
        по коду задачи - 'Лучшее средство'.
        Тест проверяет, что:
        - осуществляется добавление ключа 'Количество средств'
        - правильное количество средств
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                         'Средство_2': 'OUSHEN Curl & shine shampoo',
                         'Средство_3': 'NATURA SIBERICA Oblepikha',
                         'Средство_4': 'WELEDA Millet Nourishing',
                         'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                         'Средство_6': 'LADOR Keratin LPP'},
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1'}

        # Ожидаемое количество ключей ДО обработки
        original_keys_count = len(data_collection.keys())

        # Инициализация объекта и вызов метода
        json_proc_data = JsonProcessingData(data_collection=data_collection)
        result = json_proc_data.distribution_on_task()
        # pprint(result)

        # Ожидаемый результат
        expected_result = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {
                'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                'Средство_2': 'OUSHEN Curl & shine shampoo',
                'Средство_3': 'NATURA SIBERICA Oblepikha',
                'Средство_4': 'WELEDA Millet Nourishing',
                'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                'Средство_6': 'LADOR Keratin LPP'
            },
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
            'Количество средств': 6
        }

        # Проверка, что добавился ключ 'Количество средств'
        self.assertIn('Количество средств', result,
                      msg="Отсутствует ключ 'Количество средств'")

        # Проверка, что значение количества средств корректно
        self.assertEqual(result['Количество средств'], 6,
                         msg="Некорректное значение ключа 'Количество средств'")

        # Проверка, что добавился ровно один ключ
        self.assertEqual(len(result.keys()), original_keys_count + 1,
                         msg="Добавилось больше одного нового ключа")

        # Проверка, что результат равен ожидаемому
        self.assertEqual(result, expected_result,
                         msg="Результат обработки не совпадает с ожидаемым словарём")

    def test_get_json_scheme_for_best_product(self):
        """
        Проверка метода get_json_scheme_for_distribution_on_task:
        - корректное формирование json-схемы для задачи 'Лучшее средство'
        """

        # Подготовка данных
        data_collection = {
            'Возраст': 32,
            'Задача': 'Лучшее средство',
            'Запрос': 'ЗВ8, ЗВ12',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'Шампуни',
            'Специалист': 'Т',
            'Средства': {
                'Средство_1': 'ALTEREGO ITALY Curego Hydraday',
                'Средство_2': 'OUSHEN Curl & shine shampoo',
                'Средство_3': 'NATURA SIBERICA Oblepikha',
                'Средство_4': 'WELEDA Millet Nourishing',
                'Средство_5': 'PAYOT Shampoing doux biome-friendly',
                'Средство_6': 'LADOR Keratin LPP'
            },
            'Тип': 'В1, В10',
            'Хеш': '6157254f8a165e4f6baa6a45ee2ca32042b8de1d6a19680d11879ab43c7a5cd1',
            'Количество средств': 6
        }

        # product_categories можно пустым (если в этой логике не участвует)
        product_categories = {}

        # Ожидаемая схема
        expected_schema = {
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
                    },
                    "product_1": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Название 1-го средства"
                            },
                            "plus": {
                                "type": "string",
                                "description":
                                    "Описание плюсов 1-го средства (без названия средства)"
                            },
                            "minus": {
                                "type": "string",
                                "description":
                                    "Описание минусов 1-го средства (без названия средства)"
                            },
                            "best_product": {
                                "type": "boolean",
                                "description": "Если это средство стало лучшим, "
                                               "поставь здесь True, если нет, то False"
                            }
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    },
                    "product_2": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Название 2-го средства",
                            },
                            "plus": {
                                "type": "string",
                                "description": "Описание плюсов 2-го средства (без названия средства)",
                            },
                            "minus": {
                                "type": "string",
                                "description": "Описание минусов 2-го средства (без названия средства)",
                            },
                            "best_product": {
                                "type": "boolean",
                                "description": "Если это средство стало лучшим, "
                                               "поставь здесь True, если нет, то False"}
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    },
                    "product_3": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string", "description": "Название 3-го средства"},
                            "plus": {
                                "type": "string",
                                "description": "Описание плюсов 3-го средства (без названия средства)"},
                            "minus": {
                                "type": "string",
                                "description": "Описание минусов 3-го средства (без названия средства)"},
                            "best_product": {
                                "type": "boolean",
                                "description": "Если это средство стало лучшим, "
                                               "поставь здесь True, если нет, то False"}
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    },
                    "product_4": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Название 4-го средства"},
                            "plus": {"type": "string",
                                     "description": "Описание плюсов 4-го средства (без названия средства)"},
                            "minus": {"type": "string",
                                      "description": "Описание минусов 4-го средства (без названия средства)"},
                            "best_product": {"type": "boolean",
                                             "description": "Если это средство стало лучшим, "
                                                            "поставь здесь True, если нет, то False"}
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    },
                    "product_5": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string", "description": "Название 5-го средства"},
                            "plus": {
                                "type": "string",
                                "description": "Описание плюсов 5-го средства (без названия средства)"},
                            "minus": {
                                "type": "string",
                                "description": "Описание минусов 5-го средства (без названия средства)"},
                            "best_product": {
                                "type": "boolean",
                                "description": "Если это средство стало лучшим, "
                                               "поставь здесь True, если нет, то False"}
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    },
                    "product_6": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string", "description": "Название 6-го средства"},
                            "plus": {
                                "type": "string",
                                "description": "Описание плюсов 6-го средства (без названия средства)"},
                            "minus": {
                                "type": "string",
                                "description": "Описание минусов 6-го средства (без названия средства)"},
                            "best_product": {
                                "type": "boolean",
                                "description": "Если это средство стало лучшим, "
                                               "поставь здесь True, если нет, то False"}
                        },
                        "required": ["title", "plus", "minus", "best_product"],
                        "additionalProperties": False
                    }
                },
                "required": [
                    "best_product",
                    "result",
                    "product_1",
                    "product_2",
                    "product_3",
                    "product_4",
                    "product_5",
                    "product_6"
                ],
                "additionalProperties": False
            }
        }

        # Инициализация JsonCreator и получение схемы
        json_creator = JsonCreator(
            data_collection=data_collection,
            product_categories=product_categories
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()

        # Проверка, что схема совпадает с ожидаемой
        self.assertEqual(actual_schema, expected_schema, msg="Схема не совпадает с ожидаемой")

    def test_decryption_task_one_product(self):
        """
        Проверка работы метода для преобразования словаря
        по коду задачи - 'Лучшее средство'.
        """

        data_collection = {
            'Возраст': 32,
            'Задача': 'Разбор состава одного средства',
            'Запрос': 'ЗЛ2',
            'Итог': None,
            'Лучший вариант': None,
            'Пол': 'женский',
            'Категория': 'уход за кожей лица',
            'Специалист': 'Т',
            'Средства': {'Средство_1': 'ALTEREGO ITALY Curego Hydraday'},
            'Тип': 'КЛ1',
            'Хеш': '1cf5f44310b2ea42c5b498aef5a314dcea315cf69f4a6d97c96101ea8e517229'
        }

        # Ожидаемая схема без вложенности
        expected_schema = {
            "name": "cosmetic_product_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    # Базовые поля
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
                        "description": "Подробно поясни суть увлажняющих и ухаживающих компонентов"
                    },
                    "preservatives_and_ph_regulators": {
                        "type": "string",
                        "description": "Подробно поясни суть консервантов и регуляторов pH, если они есть"
                    },
                    "banned_or_unwanted": {
                        "type": "string",
                        "description": "Подробно поясни суть запрещенных или нежелательных компонентов"
                    },
                    "additional_properties": {
                        "type": "string",
                        "description": "Если есть какие-то дополнительные свойства, укажи их и поясни"
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
                    "result": {
                        "type": "string",
                        "description": "Вывод, исходя из всей вышепредставленной информации"
                    },
                    # Дополнительные поля из facial_skin_care
                    "skin_type_impact": {
                        "type": "string",
                        "description": "Влияние на тип кожи (комедогенность, увлажнение)"
                    },
                    "spf_level": {
                        "type": "string",
                        "description": "Уровень SPF (если есть)"
                    },
                    "application_time": {
                        "type": "string",
                        "description": "Время нанесения (если требуется выдержка)"
                    },
                    "ph_level": {
                        "type": "string",
                        "description": "Уровень pH"
                    },
                    "exfoliation_intensity": {
                        "type": "string",
                        "description": "Интенсивность пилинга (для скрабов)"
                    },
                    "eye_area_effect": {
                        "type": "string",
                        "description": "Эффект на область глаз (для патчей)"
                    }
                },
                "required": [
                    # Список всех полей
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
                    "result",
                    "skin_type_impact",
                    "spf_level",
                    "application_time",
                    "ph_level",
                    "exfoliation_intensity",
                    "eye_area_effect"
                ],
                "additionalProperties": False
            }
        }

        # на этом этапе по этому ключу ничего не происходит в функции
        json_proc_data = JsonProcessingData(data_collection=data_collection)
        update_data_collection = json_proc_data.distribution_on_task()

        # Создание экземпляра класса по созданию json-схемы
        json_creator = JsonCreator(
            data_collection=update_data_collection,
            product_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
        )

        actual_schema = json_creator.get_json_scheme_for_distribution_on_task()

        # Проверка результата
        self.assertEqual(actual_schema, expected_schema, msg="Схема не совпадает с ожидаемой")
