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
                'метод создает json-схему для текущей подборки по коду задачи',
            'Разбор состава одного средства': self.create_json_scheme_for_one_product,
            'Лучшая пара': 'метод создает json-схему для текущей подборки по коду задачи',
            'Лучшее сочетание': 'метод создает json-схему для текущей подборки по коду задачи',
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
            product_properties = schema["schema"]["properties"]["product"]["properties"]
            product_required = schema["schema"]["properties"]["product"]["required"]

            product_properties.update(extension_schema["properties"])
            product_required.extend(extension_schema["required"])

        return schema
