# pylint: skip-file

# В этом модуле константы для тестов json конструктора

expected_schema_for_best_product = {
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

# ожидаемая схема для 1 продукта для категории - уход за кожей лица
# проверить, что всё добавляется
expected_schema_for_one_product = {
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

expected_schema_for_best_prod_carcinogen = {
    'name': 'cosmetics_analysis',
    'schema': {
        'additionalProperties': False,
        'properties':
            {'best_product': {'description': 'Лучшее средство',
                              'type': 'string'},
             'product_1': {'additionalProperties': False,
                           'properties': {'best_product': {'description': 'Если '
                                                                          'это '
                                                                          'средство '
                                                                          'стало '
                                                                          'лучшим, '
                                                                          'поставь '
                                                                          'здесь '
                                                                          'True, '
                                                                          'если '
                                                                          'нет, '
                                                                          'то '
                                                                          'False',
                                                           'type': 'boolean'},
                                          'carcinogen': {'description': 'Названия '
                                                                        'канцерогенов '
                                                                        '1-го '
                                                                        'средства, '
                                                                        'если '
                                                                        'они '
                                                                        'есть '
                                                                        'в '
                                                                        'составе',
                                                         'type': 'string'},
                                          'minus': {'description': 'Описание '
                                                                   'минусов '
                                                                   '1-го '
                                                                   'средства '
                                                                   '(без '
                                                                   'названия '
                                                                   'средства)',
                                                    'type': 'string'},
                                          'plus': {'description': 'Описание '
                                                                  'плюсов '
                                                                  '1-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                          'title': {'description': 'Название '
                                                                   '1-го '
                                                                   'средства',
                                                    'type': 'string'}},
                           'required': ['title',
                                        'plus',
                                        'minus',
                                        'best_product',
                                        'carcinogen'],
                           'type': 'object'},
             'product_2': {'additionalProperties': False,
                           'properties': {'best_product': {'description': 'Если '
                                                                          'это '
                                                                          'средство '
                                                                          'стало '
                                                                          'лучшим, '
                                                                          'поставь '
                                                                          'здесь '
                                                                          'True, '
                                                                          'если '
                                                                          'нет, '
                                                                          'то '
                                                                          'False',
                                                           'type': 'boolean'},
                                          'carcinogen': {'description': 'Названия '
                                                                        'канцерогенов '
                                                                        '2-го '
                                                                        'средства, '
                                                                        'если '
                                                                        'они '
                                                                        'есть '
                                                                        'в '
                                                                        'составе',
                                                         'type': 'string'},
                                          'minus': {'description': 'Описание '
                                                                   'минусов '
                                                                   '2-го '
                                                                   'средства '
                                                                   '(без '
                                                                   'названия '
                                                                   'средства)',
                                                    'type': 'string'},
                                          'plus': {'description': 'Описание '
                                                                  'плюсов '
                                                                  '2-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                          'title': {'description': 'Название '
                                                                   '2-го '
                                                                   'средства',
                                                    'type': 'string'}},
                           'required': ['title',
                                        'plus',
                                        'minus',
                                        'best_product',
                                        'carcinogen'],
                           'type': 'object'},
             'product_3': {'additionalProperties': False,
                           'properties': {'best_product': {'description': 'Если '
                                                                          'это '
                                                                          'средство '
                                                                          'стало '
                                                                          'лучшим, '
                                                                          'поставь '
                                                                          'здесь '
                                                                          'True, '
                                                                          'если '
                                                                          'нет, '
                                                                          'то '
                                                                          'False',
                                                           'type': 'boolean'},
                                          'carcinogen': {'description': 'Названия '
                                                                        'канцерогенов '
                                                                        '3-го '
                                                                        'средства, '
                                                                        'если '
                                                                        'они '
                                                                        'есть '
                                                                        'в '
                                                                        'составе',
                                                         'type': 'string'},
                                          'minus': {'description': 'Описание '
                                                                   'минусов '
                                                                   '3-го '
                                                                   'средства '
                                                                   '(без '
                                                                   'названия '
                                                                   'средства)',
                                                    'type': 'string'},
                                          'plus': {'description': 'Описание '
                                                                  'плюсов '
                                                                  '3-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                          'title': {'description': 'Название '
                                                                   '3-го '
                                                                   'средства',
                                                    'type': 'string'}},
                           'required': ['title',
                                        'plus',
                                        'minus',
                                        'best_product',
                                        'carcinogen'],
                           'type': 'object'},
             'product_4': {'additionalProperties': False,
                           'properties': {'best_product': {'description': 'Если '
                                                                          'это '
                                                                          'средство '
                                                                          'стало '
                                                                          'лучшим, '
                                                                          'поставь '
                                                                          'здесь '
                                                                          'True, '
                                                                          'если '
                                                                          'нет, '
                                                                          'то '
                                                                          'False',
                                                           'type': 'boolean'},
                                          'carcinogen': {'description': 'Названия '
                                                                        'канцерогенов '
                                                                        '4-го '
                                                                        'средства, '
                                                                        'если '
                                                                        'они '
                                                                        'есть '
                                                                        'в '
                                                                        'составе',
                                                         'type': 'string'},
                                          'minus': {'description': 'Описание '
                                                                   'минусов '
                                                                   '4-го '
                                                                   'средства '
                                                                   '(без '
                                                                   'названия '
                                                                   'средства)',
                                                    'type': 'string'},
                                          'plus': {'description': 'Описание '
                                                                  'плюсов '
                                                                  '4-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                          'title': {'description': 'Название '
                                                                   '4-го '
                                                                   'средства',
                                                    'type': 'string'}},
                           'required': ['title',
                                        'plus',
                                        'minus',
                                        'best_product',
                                        'carcinogen'],
                           'type': 'object'},
             'result': {'description': 'Итоговая рекомендация, '
                                       'вывод',
                        'type': 'string'}},
        'required': ['best_product',
                     'result',
                     'product_1',
                     'product_2',
                     'product_3',
                     'product_4'],
        'type': 'object'},
    'strict': True}

best_combination_json = {
    'name': 'cosmetics_analysis',
    'schema': {
        'additionalProperties': False,
        'properties':
            {'best_combination': {'description': 'Название '
                                                 'одного '
                                                 'средства из '
                                                 'списка, '
                                                 'которое лучше '
                                                 'всего '
                                                 'сочетается с '
                                                 'исходным.',
                                  'type': 'string'},
             'origin_product': {'description': 'Исходное '
                                               'средство, к '
                                               'которому '
                                               'подбирается '
                                               'сочетание',
                                'type': 'string'},
             'product_1': {'additionalProperties': False,
                           'properties': {
                               'best_combination': {'description': 'Если '
                                                                   'это '
                                                                   'средство '
                                                                   'попало '
                                                                   'в '
                                                                   'сочетание '
                                                                   'с '
                                                                   'исходным, '
                                                                   'поставь '
                                                                   'здесь '
                                                                   'True, '
                                                                   'иначе '
                                                                   'False',
                                                    'type': 'boolean'},
                               'result': {'description': 'Объяснение, '
                                                         'почему '
                                                         'выбрали '
                                                         'или '
                                                         'не '
                                                         'выбрали '
                                                         'это '
                                                         'средство.',
                                          'type': 'string'},
                               'title': {'description': 'Название '
                                                        '1-го '
                                                        'средства',
                                         'type': 'string'}},
                           'required': ['title',
                                        'result',
                                        'best_combination'],
                           'type': 'object'},
             'product_2': {'additionalProperties': False,
                           'properties': {
                               'best_combination': {'description': 'Если '
                                                                   'это '
                                                                   'средство '
                                                                   'попало '
                                                                   'в '
                                                                   'сочетание '
                                                                   'с '
                                                                   'исходным, '
                                                                   'поставь '
                                                                   'здесь '
                                                                   'True, '
                                                                   'иначе '
                                                                   'False',
                                                    'type': 'boolean'},
                               'result': {'description': 'Объяснение, '
                                                         'почему '
                                                         'выбрали '
                                                         'или '
                                                         'не '
                                                         'выбрали '
                                                         'это '
                                                         'средство.',
                                          'type': 'string'},
                               'title': {'description': 'Название '
                                                        '2-го '
                                                        'средства',
                                         'type': 'string'}},
                           'required': ['title',
                                        'result',
                                        'best_combination'],
                           'type': 'object'},
             'product_3': {'additionalProperties': False,
                           'properties': {
                               'best_combination': {'description': 'Если '
                                                                   'это '
                                                                   'средство '
                                                                   'попало '
                                                                   'в '
                                                                   'сочетание '
                                                                   'с '
                                                                   'исходным, '
                                                                   'поставь '
                                                                   'здесь '
                                                                   'True, '
                                                                   'иначе '
                                                                   'False',
                                                    'type': 'boolean'},
                               'result': {'description': 'Объяснение, '
                                                         'почему '
                                                         'выбрали '
                                                         'или '
                                                         'не '
                                                         'выбрали '
                                                         'это '
                                                         'средство.',
                                          'type': 'string'},
                               'title': {'description': 'Название '
                                                        '3-го '
                                                        'средства',
                                         'type': 'string'}},
                           'required': ['title',
                                        'result',
                                        'best_combination'],
                           'type': 'object'},
             'result': {'description': 'Итоговая рекомендация, '
                                       'вывод',
                        'type': 'string'}},
        'required': ['origin_product',
                     'best_combination',
                     'result',
                     'product_1',
                     'product_2',
                     'product_3'],
        'type': 'object'},
    'strict': True,
}

best_set_json = {
    'name': 'cosmetics_analysis',
    'schema': {'additionalProperties': False,
               'properties': {'best_pair': {'description': 'Названия средств '
                                                           'внутри пары, которая '
                                                           'считается лучшей '
                                                           'среди всех '
                                                           'предложенных',
                                            'type': 'string'},
                              'pair_1': {'additionalProperties': False,
                                         'properties': {'best_pair': {'description': 'Если '
                                                                                     'эта '
                                                                                     'пара '
                                                                                     'средств '
                                                                                     'выбрана '
                                                                                     'как '
                                                                                     'лучшая '
                                                                                     'среди '
                                                                                     'всех '
                                                                                     'пар, '
                                                                                     'поставь '
                                                                                     'здесь '
                                                                                     'True; '
                                                                                     'если '
                                                                                     'нет '
                                                                                     '— '
                                                                                     'False',
                                                                      'type': 'boolean'},
                                                        'product_1': {'description': 'Название '
                                                                                     'средства '
                                                                                     '№1 '
                                                                                     'из '
                                                                                     'пары '
                                                                                     '№1',
                                                                      'type': 'string'},
                                                        'product_2': {'description': 'Название '
                                                                                     'средства '
                                                                                     '№2 '
                                                                                     'из '
                                                                                     'пары '
                                                                                     '№1',
                                                                      'type': 'string'},
                                                        'result': {'description': 'Объяснение, '
                                                                                  'почему '
                                                                                  'эта '
                                                                                  'пара '
                                                                                  'выбрана '
                                                                                  'как '
                                                                                  'лучшая '
                                                                                  'или '
                                                                                  'почему '
                                                                                  'нет',
                                                                   'type': 'string'},
                                                        'title': {'description': 'Названия '
                                                                                 'двух '
                                                                                 'средств '
                                                                                 'из '
                                                                                 'пары '
                                                                                 '№1, '
                                                                                 'перечисленные '
                                                                                 'через '
                                                                                 'запятую',
                                                                  'type': 'string'}},
                                         'required': ['title',
                                                      'result',
                                                      'best_pair'],
                                         'type': 'object'},
                              'pair_2': {'additionalProperties': False,
                                         'properties': {'best_pair': {'description': 'Если '
                                                                                     'эта '
                                                                                     'пара '
                                                                                     'средств '
                                                                                     'выбрана '
                                                                                     'как '
                                                                                     'лучшая '
                                                                                     'среди '
                                                                                     'всех '
                                                                                     'пар, '
                                                                                     'поставь '
                                                                                     'здесь '
                                                                                     'True; '
                                                                                     'если '
                                                                                     'нет '
                                                                                     '— '
                                                                                     'False',
                                                                      'type': 'boolean'},
                                                        'product_1': {'description': 'Название '
                                                                                     'средства '
                                                                                     '№1 '
                                                                                     'из '
                                                                                     'пары '
                                                                                     '№2',
                                                                      'type': 'string'},
                                                        'product_2': {'description': 'Название '
                                                                                     'средства '
                                                                                     '№2 '
                                                                                     'из '
                                                                                     'пары '
                                                                                     '№2',
                                                                      'type': 'string'},
                                                        'result': {'description': 'Объяснение, '
                                                                                  'почему '
                                                                                  'эта '
                                                                                  'пара '
                                                                                  'выбрана '
                                                                                  'как '
                                                                                  'лучшая '
                                                                                  'или '
                                                                                  'почему '
                                                                                  'нет',
                                                                   'type': 'string'},
                                                        'title': {'description': 'Названия '
                                                                                 'двух '
                                                                                 'средств '
                                                                                 'из '
                                                                                 'пары '
                                                                                 '№2, '
                                                                                 'перечисленные '
                                                                                 'через '
                                                                                 'запятую',
                                                                  'type': 'string'}},
                                         'required': ['title',
                                                      'result',
                                                      'best_pair'],
                                         'type': 'object'},
                              'result': {'description': 'Итоговая рекомендация по '
                                                        'лучшей паре, вывод',
                                         'type': 'string'}},
               'required': ['best_pair', 'result', 'pair_1', 'pair_2'],
               'type': 'object'},
    'strict': True}
