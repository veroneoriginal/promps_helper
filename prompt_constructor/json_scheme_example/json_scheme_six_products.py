JSON_SCHEME_SIX_PRODUCTS = {
    "name": "cosmetics_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "best_product": {
                "type": "string",
                "description": "Лучшее средство"
            },
            "product_1": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название первого средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов первого средства (без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов первого средства (без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "product_2": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название второго средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов второго средства (без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов второго средства (без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "product_3": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название третьего средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов третьего средства (без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов третьего средства (без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "product_4": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название четвертого средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов четвертого средства "
                                       "(без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов четвертого средства "
                                       "(без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "product_5": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название пятого средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов пятого средства "
                                       "(без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов пятого средства "
                                       "(без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "product_6": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Название шестого средства"
                    },
                    "plus": {
                        "type": "string",
                        "description": "Описание плюсов шестого средства (без названия средства)"
                    },
                    "minus": {
                        "type": "string",
                        "description": "Описание минусов шестого средства (без названия средства)"
                    }
                },
                "required": [
                    "title",
                    "plus",
                    "minus"
                ],
                "additionalProperties": False
            },
            "result": {
                "type": "string",
                "description": "Итоговая рекомендация, вывод"
            }
        },
        "required": [
            "best_product",
            "product_1",
            "product_2",
            "product_3",
            "product_4",
            "product_5",
            "product_6",
            "result"
        ],
        "additionalProperties": False
    }
}
