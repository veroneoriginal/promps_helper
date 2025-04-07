# pylint: skip-file

# В этом модуле константы для тестов json конструктора

EXPECTED_SCHEMA_FOR_ANALOGUE_PRODUCT = {
    'name': 'analog_product',
    'schema': {
        'additionalProperties': False,
        'properties': {
            'analog_product': {
                'additionalProperties': False,
                'properties': {
                    'article': {
                        'description': 'Артикул '
                                       'средства-аналога, '
                                       'только '
                                       'цифры.',
                        'type': 'string'},
                    'title': {
                        'description': 'Название '
                                       'средства-аналога',
                        'type': 'string'}},
                'required': ['title', 'article'],
                'type': 'object'},
            'differences': {'description': 'Здесь укажи '
                                           'различия средств, '
                                           'чем они отличаются',
                            'type': 'string'},
            'result': {'description': 'Итоговый вывод подробно',
                       'type': 'string'},
            'short_result': {'description': 'Итоговый вывод '
                                            'коротко',
                             'type': 'string'},
            'similarities': {'description': 'Здесь укажи '
                                            'сходства средств, '
                                            'что у них общего',
                             'type': 'string'},
            'source_product': {'additionalProperties': False,
                               'properties': {'article': {
                                   'description': 'Артикул '
                                                  'исходного '
                                                  'средства, '
                                                  'только '
                                                  'цифры.',
                                   'type': 'string'},
                                   'title': {
                                       'description': 'Название '
                                                      'исходного '
                                                      'средства',
                                       'type': 'string'}},
                               'required': ['title', 'article'],
                               'type': 'object'}},
        'required': ['result',
                     'short_result',
                     'similarities',
                     'differences',
                     'source_product',
                     'analog_product'],
        'type': 'object'},
    'strict': True}

EXPECTED_SCHEMA_FOR_BEST_PRODUCT = {
    'name': 'best_product',
    'schema': {
        'additionalProperties': False,
        'properties': {
            'product_1': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '1-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'product_2': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '2-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'product_3': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '3-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'product_4': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '4-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'product_5': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '5-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                         'minus': {'description': 'Описание '
                                                                  'минусов '
                                                                  '5-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                         'plus': {'description': 'Описание '
                                                                 'плюсов '
                                                                 '5-го '
                                                                 'средства '
                                                                 '(без '
                                                                 'названия '
                                                                 'средства)',
                                                  'type': 'string'},
                                         'title': {'description': 'Название '
                                                                  '5-го '
                                                                  'средства',
                                                   'type': 'string'}},
                          'required': ['title',
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'product_6': {'additionalProperties': False,
                          'properties': {'article': {'description': 'Артикул '
                                                                    '6-го '
                                                                    'средства, '
                                                                    'только '
                                                                    'цифры.',
                                                     'type': 'string'},
                                         'best_product': {'description': 'Если '
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
                                         'minus': {'description': 'Описание '
                                                                  'минусов '
                                                                  '6-го '
                                                                  'средства '
                                                                  '(без '
                                                                  'названия '
                                                                  'средства)',
                                                   'type': 'string'},
                                         'plus': {'description': 'Описание '
                                                                 'плюсов '
                                                                 '6-го '
                                                                 'средства '
                                                                 '(без '
                                                                 'названия '
                                                                 'средства)',
                                                  'type': 'string'},
                                         'title': {'description': 'Название '
                                                                  '6-го '
                                                                  'средства',
                                                   'type': 'string'}},
                          'required': ['title',
                                       'article',
                                       'plus',
                                       'minus',
                                       'best_product'],
                          'type': 'object'},
            'result': {'description': 'Итоговая рекомендация, '
                                      'вывод',
                       'type': 'string'}},
        'required': ['result',
                     'product_1',
                     'product_2',
                     'product_3',
                     'product_4',
                     'product_5',
                     'product_6'],
        'type': 'object'},
    'strict': True}

# ожидаемая схема для 1 продукта для категории - уход за кожей лица
# проверить, что всё добавляется
EXPECTED_SCHEMA_FOR_ONE_PRODUCT = {
    "name": "one_product",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            # Базовые поля
            "title": {
                "type": "string",
                "description": "Название средства"
            },
            'article': {'description': 'Артикул средства',
                        'type': 'string'},
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
            "additional_components": {
                "type": "string",
                "description": "Если есть какие-то дополнительные компоненты, укажи их и поясни"
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
            "article",
            "main_components",
            "active_ingredients",
            "moisturizing_and_care",
            "preservatives_and_ph_regulators",
            "banned_or_unwanted",
            "additional_components",
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

EXPECTED_SCHEMA_FOR_BEST_PROD_CARCINOGEN = {
    'name': 'carcinogen_free',
    'schema': {'additionalProperties': False,
               'properties': {'product_1': {'additionalProperties': False,
                                            'properties': {'article': {'description': 'Артикул '
                                                                                      '1-го '
                                                                                      'средства, '
                                                                                      'только '
                                                                                      'цифры.',
                                                                       'type': 'string'},
                                                           'best_product': {'description': 'Если '
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
                                                                                         'составе. '
                                                                                         'Если '
                                                                                         'нет '
                                                                                         '- '
                                                                                         'оставь '
                                                                                         'пустой '
                                                                                         'строкой',
                                                                          'type': 'string'},
                                                           'influence_of_carcinogens': {'description': 'Опиши '
                                                                                                       'подробно, '
                                                                                                       'на '
                                                                                                       'что '
                                                                                                       'и '
                                                                                                       'как '
                                                                                                       'влияют '
                                                                                                       'канцерогены '
                                                                                                       'в '
                                                                                                       'организме '
                                                                                                       'человека, '
                                                                                                       'найденные '
                                                                                                       'в '
                                                                                                       'средстве '
                                                                                                       '1, '
                                                                                                       'если '
                                                                                                       'они '
                                                                                                       'найдены '
                                                                                                       'в '
                                                                                                       'составе.Пиши '
                                                                                                       'с '
                                                                                                       'названиями '
                                                                                                       'канцирогенов.',
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
                                                         'article',
                                                         'plus',
                                                         'minus',
                                                         'best_product',
                                                         'carcinogen',
                                                         'influence_of_carcinogens'],
                                            'type': 'object'},
                              'product_2': {'additionalProperties': False,
                                            'properties': {'article': {'description': 'Артикул '
                                                                                      '2-го '
                                                                                      'средства, '
                                                                                      'только '
                                                                                      'цифры.',
                                                                       'type': 'string'},
                                                           'best_product': {'description': 'Если '
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
                                                                                         'составе. '
                                                                                         'Если '
                                                                                         'нет '
                                                                                         '- '
                                                                                         'оставь '
                                                                                         'пустой '
                                                                                         'строкой',
                                                                          'type': 'string'},
                                                           'influence_of_carcinogens': {'description': 'Опиши '
                                                                                                       'подробно, '
                                                                                                       'на '
                                                                                                       'что '
                                                                                                       'и '
                                                                                                       'как '
                                                                                                       'влияют '
                                                                                                       'канцерогены '
                                                                                                       'в '
                                                                                                       'организме '
                                                                                                       'человека, '
                                                                                                       'найденные '
                                                                                                       'в '
                                                                                                       'средстве '
                                                                                                       '2, '
                                                                                                       'если '
                                                                                                       'они '
                                                                                                       'найдены '
                                                                                                       'в '
                                                                                                       'составе.Пиши '
                                                                                                       'с '
                                                                                                       'названиями '
                                                                                                       'канцирогенов.',
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
                                                         'article',
                                                         'plus',
                                                         'minus',
                                                         'best_product',
                                                         'carcinogen',
                                                         'influence_of_carcinogens'],
                                            'type': 'object'},
                              'product_3': {'additionalProperties': False,
                                            'properties': {'article': {'description': 'Артикул '
                                                                                      '3-го '
                                                                                      'средства, '
                                                                                      'только '
                                                                                      'цифры.',
                                                                       'type': 'string'},
                                                           'best_product': {'description': 'Если '
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
                                                                                         'составе. '
                                                                                         'Если '
                                                                                         'нет '
                                                                                         '- '
                                                                                         'оставь '
                                                                                         'пустой '
                                                                                         'строкой',
                                                                          'type': 'string'},
                                                           'influence_of_carcinogens': {'description': 'Опиши '
                                                                                                       'подробно, '
                                                                                                       'на '
                                                                                                       'что '
                                                                                                       'и '
                                                                                                       'как '
                                                                                                       'влияют '
                                                                                                       'канцерогены '
                                                                                                       'в '
                                                                                                       'организме '
                                                                                                       'человека, '
                                                                                                       'найденные '
                                                                                                       'в '
                                                                                                       'средстве '
                                                                                                       '3, '
                                                                                                       'если '
                                                                                                       'они '
                                                                                                       'найдены '
                                                                                                       'в '
                                                                                                       'составе.Пиши '
                                                                                                       'с '
                                                                                                       'названиями '
                                                                                                       'канцирогенов.',
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
                                                         'article',
                                                         'plus',
                                                         'minus',
                                                         'best_product',
                                                         'carcinogen',
                                                         'influence_of_carcinogens'],
                                            'type': 'object'},
                              'product_4': {'additionalProperties': False,
                                            'properties': {'article': {'description': 'Артикул '
                                                                                      '4-го '
                                                                                      'средства, '
                                                                                      'только '
                                                                                      'цифры.',
                                                                       'type': 'string'},
                                                           'best_product': {'description': 'Если '
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
                                                                                         'составе. '
                                                                                         'Если '
                                                                                         'нет '
                                                                                         '- '
                                                                                         'оставь '
                                                                                         'пустой '
                                                                                         'строкой',
                                                                          'type': 'string'},
                                                           'influence_of_carcinogens': {'description': 'Опиши '
                                                                                                       'подробно, '
                                                                                                       'на '
                                                                                                       'что '
                                                                                                       'и '
                                                                                                       'как '
                                                                                                       'влияют '
                                                                                                       'канцерогены '
                                                                                                       'в '
                                                                                                       'организме '
                                                                                                       'человека, '
                                                                                                       'найденные '
                                                                                                       'в '
                                                                                                       'средстве '
                                                                                                       '4, '
                                                                                                       'если '
                                                                                                       'они '
                                                                                                       'найдены '
                                                                                                       'в '
                                                                                                       'составе.Пиши '
                                                                                                       'с '
                                                                                                       'названиями '
                                                                                                       'канцирогенов.',
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
                                                         'article',
                                                         'plus',
                                                         'minus',
                                                         'best_product',
                                                         'carcinogen',
                                                         'influence_of_carcinogens'],
                                            'type': 'object'},
                              'result': {'description': 'Итоговая рекомендация, '
                                                        'вывод',
                                         'type': 'string'}},
               'required': ['result',
                            'product_1',
                            'product_2',
                            'product_3',
                            'product_4'],
               'type': 'object'},
    'strict': True}

BEST_COMBINATION_JSON = {
    'name': 'best_combination',
    'strict': True, 'schema': {
        'type': 'object', 'properties': {
            'origin_product': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string', 'description': 'Название исходного средства'
                    },
                    'article': {
                        'type': 'string',
                        'description': 'Артикул исходного средства, только цифры.'
                    },
                    'plus': {'type': 'string',
                             'description': 'Описание плюсов исходного средства (без названия средства)'},
                    'minus': {'type': 'string',
                              'description': 'Описание минусов исходного средства (без названия средства)'}},
                'required': ['title', 'article', 'plus', 'minus'], 'additionalProperties': False},
            'result': {'type': 'string', 'description': 'Итоговая рекомендация, вывод'},
            'product_1': {'type': 'object',
                          'properties': {'title': {
                              'type': 'string',
                              'description': 'Название 1-го средства'},
                              'article': {
                                  'type': 'string',
                                  'description': 'Артикул средства, только цифры.'},
                              'plus': {
                                  'type': 'string',
                                  'description': 'Описание плюсов средства'},
                              'minus': {
                                  'type': 'string',
                                  'description': 'Описание минусов средства'},
                              'result': {
                                  'type': 'string',
                                  'description': 'Объяснение, почему выбрали или не выбрали это средство.'},
                              'best_product': {
                                  'type': 'boolean',
                                  'description': 'Если это средство попало в сочетание с исходным, поставь здесь True, иначе False'}},
                          'required': ['title',
                                       'article',
                                       'plus',
                                       'minus',
                                       'result',
                                       'best_product'],
                          'additionalProperties': False},
            'product_2': {
                'type': 'object', 'properties': {'title': {'type': 'string', 'description': 'Название 2-го средства'},
                                                 'article': {'type': 'string',
                                                             'description': 'Артикул средства, только цифры.'},
                                                 'plus': {'type': 'string',
                                                          'description': 'Описание плюсов средства'},
                                                 'minus': {'type': 'string',
                                                           'description': 'Описание минусов средства'},
                                                 'result': {'type': 'string',
                                                            'description': 'Объяснение, почему выбрали или не выбрали это средство.'},
                                                 'best_product': {'type': 'boolean',
                                                                  'description': 'Если это средство попало в сочетание с исходным, поставь здесь True, иначе False'}},
                'required': ['title', 'article', 'plus', 'minus', 'result', 'best_product'],
                'additionalProperties': False}}, 'required': ['origin_product', 'result', 'product_1', 'product_2'],
        'additionalProperties': False}}

BEST_SET_JSON = {
    'name': 'best_set',
    'strict': True, 'schema': {
        'type': 'object',
        'properties': {'result': {'type': 'string', 'description': 'Итоговая рекомендация по лучшему набору, вывод'},
                       'set_1': {'type': 'object', 'properties': {'result': {'type': 'string',
                                                                             'description': 'Объяснение, почему этот набор выбран как лучший, или почему он не выбран'},
                                                                  'best_set': {'type': 'boolean',
                                                                               'description': 'Если этот набор выбран как лучший среди всех, поставь True; если нет — False'},
                                                                  'product_1': {'type': 'object', 'properties': {
                                                                      'title': {'type': 'string',
                                                                                'description': 'Название средства №1'},
                                                                      'article': {'type': 'string',
                                                                                  'description': 'Артикул средства №1, только цифры'}},
                                                                                'required': ['title', 'article'],
                                                                                'additionalProperties': False},
                                                                  'product_2': {'type': 'object', 'properties': {
                                                                      'title': {'type': 'string',
                                                                                'description': 'Название средства №2'},
                                                                      'article': {'type': 'string',
                                                                                  'description': 'Артикул средства №2, только цифры'}},
                                                                                'required': ['title', 'article'],
                                                                                'additionalProperties': False}},
                                 'required': ['result', 'best_set', 'product_1', 'product_2'],
                                 'additionalProperties': False}, 'set_2': {'type': 'object', 'properties': {
                'result': {'type': 'string',
                           'description': 'Объяснение, почему этот набор выбран как лучший, или почему он не выбран'},
                'best_set': {'type': 'boolean',
                             'description': 'Если этот набор выбран как лучший среди всех, поставь True; если нет — False'},
                'product_1': {'type': 'object',
                              'properties': {'title': {'type': 'string', 'description': 'Название средства №1'},
                                             'article': {'type': 'string',
                                                         'description': 'Артикул средства №1, только цифры'}},
                              'required': ['title', 'article'], 'additionalProperties': False},
                'product_2': {'type': 'object',
                              'properties': {'title': {'type': 'string', 'description': 'Название средства №2'},
                                             'article': {'type': 'string',
                                                         'description': 'Артикул средства №2, только цифры'}},
                              'required': ['title', 'article'], 'additionalProperties': False}},
                                                                           'required': ['result', 'best_set',
                                                                                        'product_1', 'product_2'],
                                                                           'additionalProperties': False}},
        'required': ['result', 'set_1', 'set_2'], 'additionalProperties': False}}
