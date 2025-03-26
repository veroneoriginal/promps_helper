class JsonCreator:
    """
    Класс, внутри которого создается json-схема для
    текущей подборки в зависимости от кода задачи.

    :param data_collection: данные подборки
    :return: json-схема для текущей подборки в зависимости от кода задачи.

    """

    def __init__(
            self,
            data_collection: dict,
            product_categories: dict,
    ):

        self.data_collection = data_collection
        self.product_categories = product_categories

        self.method_for_task_code = {
            'Лучшее средство': self.create_json_scheme_for_best_product,
            'Лучшее средство без канцерогенов':
                self.create_json_scheme_for_best_product_carcinogen_free,
            'Разбор состава одного средства': self.create_json_scheme_for_one_product,
            'Лучший набор': self.create_json_scheme_for_best_set,
            'Лучшее сочетание': self.create_json_scheme_for_best_combination,
            'Лучшая компоновка': 'метод создает json-схему для текущей подборки по коду задачи',
            'Аналог': 'метод создает json-схему для текущей подборки по коду задачи',
            'Наиболее похож': 'метод создает json-схему для текущей подборки по коду задачи',
            'Наименее похож': 'метод создает json-схему для текущей подборки по коду задачи',
        }

    def get_json_scheme_for_distribution_on_task(self):
        """
        С помощью этого метода определяю какую функцию для создания json вызывать
        """
        task = self.data_collection['Задача']
        return self.method_for_task_code[task]()

    def create_json_scheme_for_best_combination(self):
        """
        Метод для динамического формирования json-схемы
        для кода задачи 'Лучшее сочетание'

        :return: json-схема для заданного количества средств
        """

        schema = {
            "name": "cosmetics_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "origin_product": {
                        "type": "string",
                        "description": "Исходное средство, к которому подбирается сочетание"
                    },
                    "best_combination": {
                        "type": "string",
                        "description":
                            "Название одного средства из списка,"
                            " которое лучше всего сочетается с исходным."
                    },
                    "result": {
                        "type": "string",
                        "description": "Итоговая рекомендация, вывод"
                    }
                },
                "required": ["origin_product", "best_combination", "result"],
                "additionalProperties": False
            }
        }

        # Добавляем продукты динамически
        products = {}
        for i in range(1, self.data_collection["Количество средств"] + 1):
            product_key = f"product_{i}"
            products[product_key] = {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": f"Название {i}-го средства"
                    },
                    "result": {
                        "type": "string",
                        "description": "Объяснение, почему выбрали или не выбрали это средство."
                    },

                    "best_product": {
                        "type": "boolean",
                        "description": "Если это средство попало в сочетание с исходным,"
                                       " поставь здесь True, иначе False"
                    }
                },
                "required": ["title", "result", "best_product"],
                "additionalProperties": False
            }

        # Добавляем продукты в свойства схемы
        schema["schema"]["properties"].update(products)

        # Добавляем продукты в список `required`
        schema["schema"]["required"].extend(products.keys())

        return schema

    def create_json_scheme_for_best_product(
            self,
    ) -> dict:
        """
        Метод для динамического формирования json-схемы для кода задачи 'Лучшее средство'

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
        for i in range(1, self.data_collection["Количество средств"] + 1):
            product_key = f"product_{i}"
            products[product_key] = {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": f"Название {i}-го средства"
                    },
                    "article": {
                        "type": "string",
                        "description": f"Артикул {i}-го средства, только цифры."
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
                "required": ["title", "article", "plus", "minus", "best_product"],
                "additionalProperties": False
            }

        # Добавляем продукты в свойства схемы
        schema["schema"]["properties"].update(products)

        # Добавляем продукты в список `required`
        schema["schema"]["required"].extend(products.keys())

        return schema

    def create_json_scheme_for_best_product_carcinogen_free(
            self,
    ) -> dict:
        """
        Метод для динамического формирования json-схемы для кода задачи 'Лучшее средство'

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
        for i in range(1, self.data_collection["Количество средств"] + 1):
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
                    "carcinogen": {
                        "type": "string",
                        "description": f"Названия канцерогенов {i}-го средства,"
                                       f" если они есть в составе"
                    },
                    "best_product": {
                        "type": "boolean",
                        "description": "Если это средство стало лучшим, поставь здесь True,"
                                       " если нет, то False"
                    }
                },
                "required": ["title", "plus", "minus", "best_product", "carcinogen"],
                "additionalProperties": False
            }

        # Добавляем продукты в свойства схемы
        schema["schema"]["properties"].update(products)

        # Добавляем продукты в список `required`
        schema["schema"]["required"].extend(products.keys())

        return schema

    def _format_properties(
            self,
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

    def _create_base_json_scheme_for_one_product(
            self,
            properties_dict: dict,
    ) -> dict:
        """
        Функция, внутри которой создается базовая конструкция универсальной
        json-схемы для анализа одного средства, которая используется во всех категориях

        :param properties_dict: словарь с настройками дляформирования json-схемы
        :return: словарь в виде готовой json-схемы
        """

        product_schema = self._format_properties(properties_dict)

        schema = {
            "name": "cosmetic_product_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": product_schema["properties"],
                "required": product_schema["required"],
                "additionalProperties": False
            }
        }

        return schema

    def create_json_scheme_for_one_product(
            self,
    ) -> dict:
        """
        Метод для формирования json-схемы для кода задачи 'Разбор состава одного средства'

        :return: json-схема для заданного количества средств
        """

        # Получаем базовую схему
        schema = self._create_base_json_scheme_for_one_product(
            self.product_categories["Базовые настройки"]
        )

        category = self.data_collection.get("Категория")

        if category in self.product_categories:
            extension_properties = self.product_categories[category]
            extension_schema = self._format_properties(extension_properties)

            # Добавляем новые поля в schema
            product_properties = schema["schema"]["properties"]
            product_required = schema["schema"]["required"]

            product_properties.update(extension_schema["properties"])
            product_required.extend(extension_schema["required"])

        return schema

    def create_json_scheme_for_best_set(
            self,
    ) -> dict:
        """
        Метод для динамического формирования json-схемы для кода задачи 'Лучший набор'

        :return: json-схема для заданного количества наборов и средств внутри наборов
        """

        num_sets = self.data_collection.get("Количество наборов", 0)
        num_products_per_set = self.data_collection.get("Количество средств в наборе", 0)

        schema = {
            "name": "cosmetics_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "best_set": {
                        "type": "string",
                        "description":
                            "Названия средств внутри набора, который считается лучшим "
                            "среди всех предложенных."
                    },
                    "result": {
                        "type": "string",
                        "description": "Итоговая рекомендация по лучшему набору, вывод"
                    }
                },
                "required": ["best_set", "result"],
                "additionalProperties": False
            }
        }

        # Генерируем схемы для каждого набора
        for i in range(1, num_sets + 1):
            set_key = f"set_{i}"

            # Создаем словарь для описания всех средств внутри текущего набора
            product_properties = {}

            # Проходимся по каждому средству внутри набора
            for j in range(1, num_products_per_set + 1):
                # Формируем ключ для средства, например: product_1, product_2, и т.д.
                product_key = f"product_{j}"

                # Описываем свойства каждого средства
                product_properties[product_key] = {
                    "type": "string",
                    "description": f"Название средства №{j} из набора №{i}"
                }

            # Добавляем стандартные поля
            set_properties = {
                "title": {
                    "type": "string",
                    "description": f"Названия всех средств из набора №{i},"
                                   f" перечисленные через запятую"
                },
                "result": {
                    "type": "string",
                    "description": "Объяснение, почему этот набор выбран как лучший,"
                                   " или почему он не выбран"
                },
                "best_set": {
                    "type": "boolean",
                    "description": "Если этот набор выбран как лучший среди всех,"
                                   " поставь True; если нет — False"
                }
            }

            # Объединяем поля
            set_properties.update(product_properties)

            # Формируем список обязательных полей
            required_fields = ["title", "result", "best_set"] + list(product_properties.keys())

            schema["schema"]["properties"][set_key] = {
                "type": "object",
                "properties": set_properties,
                "required": required_fields,
                "additionalProperties": False
            }

            # Обязательно требуем наличие ключа для этого набора
            schema["schema"]["required"].append(set_key)

        return schema
