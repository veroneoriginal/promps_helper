class PromptProcessingData:
    """
    Класс, внутри которого расшифровываются все данные
    текущей подборки, в том числе 'средства' в зависимости от кода задачи.

    :param data_collection: данные подборки
    :return: расшифрованный словарь текущей подборки
    """

    def __init__(
            self,
            data_tools: dict,
            data_collection: dict,
    ):
        self.data_tools = data_tools
        self.data_collection = data_collection
        self.method_for_task_code = {
            'Лучшее средство': self.decrypting_info_code_best_product,
            'Лучшее средство без канцерогенов': self.decrypting_info_code_best_product,
            'Разбор состава одного средства': self.decrypting_info_code_one_product,
            'Лучшая пара': self.decrypting_best_pair,
            'Лучшее сочетание': self.decrypting_info_code_best_product,
            'Лучшая компоновка': 'метод который расшифровывает словарь для этого кода задачи',
            'Аналог': 'метод который расшифровывает словарь для этого кода задачи',
            'Наиболее похож': 'метод который расшифровывает словарь для этого кода задачи',
            'Наименее похож': 'метод который расшифровывает словарь для этого кода задачи',
        }

    def _split_and_clean_type(
            self,
            symbol: str,
            type_of_need: str | tuple,
    ) -> list:
        """
        Метод для обработки строки (значения, взятого из ячейки):
        если в строке есть определенный символ, разделяет и очищает значения,
        если символа нет, возвращает список с одним очищенным значением.

        :param symbol: символ, по которому осуществляется сплит
        :param type_of_need: строка или кортеж со значениями, например "B2, B1" или "B2"
        :return: список очищенных значений, например ['B2', 'B1'] или ['B2']
        """

        if isinstance(type_of_need, tuple):
            # Если передан кортеж, сразу превращаем его в список строк
            return [str(value).strip() for value in type_of_need if value]

        if isinstance(type_of_need, str):
            # Убираем лишние пробелы с начала и конца строки
            type_need = type_of_need.strip()

            # Проверяем, есть ли символ в строке
            if symbol in type_need:
                # Если есть символ, разделяем и очищаем значения
                values = type_need.split(symbol)
                return [value.strip() for value in values if value.strip()]

            # Если символа нет, возвращаем список с одним очищенным значением
            return [type_need] if type_need else []

        return []

    def _decrypting_data_from_cell(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> str:
        """
        Метод для расшифровки данных из блоков Тип, Запрос

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param category: категория, с который работаем
        :return: расшифрованная строка
        """

        # получение строки с содержимым, которое было в ячейке ТИП
        body_part_type = data_collection[category]

        # формирование из строки списка отдельных элементов
        list_body_part_type = self._split_and_clean_type(
            type_of_need=body_part_type,
            symbol=",",
        )

        # формирование списка словарей с расшифрованными значениями
        params = []

        # расшифровывание кодов и добавление в этот новый список
        for element in list_body_part_type:
            params.append(data[category][element])

        # преобразование списка словарей в предложения
        sentences = []
        for item in params:
            sentence = f"{item['Область применения']}: {item['Суть']}. {item['Описание']}"
            sentences.append(sentence)

        return ' '.join(sentences)

    def _decrypting_info_from_cell(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> str:
        """
        Метод для расшифровки данных из блоков Задача, Специалист

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param category: категория, с который работаем
        :return: расшифрованная строка
        """

        # получение строки с содержимым, которое было в ячейке
        body_part_type = data_collection[category]

        # обращение по полученному коду к основному словарю с содержимым
        dict_with_full_info = data[category][body_part_type]

        return f"{dict_with_full_info['Описание']}"

    def _conversion_products(
            self,
            cosmetic_products: dict,
    ) -> str:
        """
        Метод для преобразования блока со средствами, их составами и типами в читабельный текст

        :param cosmetic_products: принимает словарь со средствами, их составом и типом
        :return: возвращает читаемую строку для промпта
        """

        list_cosmetic_products = []

        for key, value in cosmetic_products.items():
            list_cosmetic_products.append(
                f"Средство №{value['Номер']} - {key}. "
                f"Состав: {value['Состав']}. Тип продукта: {value['Тип продукта']}. ")

        # строка, которая объединяет инфо о всех сред-х в единый текст блок с переносами строк
        return "\n".join(list_cosmetic_products)

    def decrypting_info_code_best_product(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> str:
        """
        Метод для расшифровки данных из блока Средства для кода задачи
        'Лучшее средство' и 'Лучшее средство без канцерогенов'

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param category: категория, с которой работаем
        :return: словарь со средствами, их типом и составом
        """

        # получение словаря с содержимым
        products_in_cell = data_collection[category]

        # pylint: disable=W0612 unused-variable
        # формируем словарь
        products_full_info = {}
        for number, (product_key, product_name) in enumerate(products_in_cell.items()):
            # ищем данные по product_name в основном data словаре
            product_data = data[category].get(product_name, {})

            products_full_info[product_name] = {
                "Номер": number + 1,
                "Тип продукта": product_data.get("Тип продукта", "Не указан"),
                "Состав": product_data.get("Состав", "Не указан"),
            }

        # преобразование словаря со средствами в строку
        return self._conversion_products(cosmetic_products=products_full_info)

    def decrypting_info_code_one_product(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> str:
        """
        Метод для расшифровки данных из блока Средства для
        кода задачи 'Разбор состава одного средства'

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param category: категория, с который работаем
        :return: словарь со средствами, их типом и составом
        """

        # получение словаря с содержимым, которое было в ячейке
        products_in_cell = data_collection[category]

        # pylint: disable=W0612 unused-variable
        # формируем словарь
        products_full_info = {}
        for number, (product_key, product_name) in enumerate(products_in_cell.items(), start=1):
            # ищем данные по product_name в основном data словаре
            product_data = data[category].get(product_name, {})

            products_full_info[product_name] = {
                "Номер": number,
                "Тип продукта": product_data.get("Тип продукта", "Не указан"),
                "Состав": product_data.get("Состав", "Не указан"),
            }

        # преобразование словаря со средствами в строку
        return self._conversion_products(cosmetic_products=products_full_info)

    def decrypting_origin_product_info(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> str:
        """
        Метод для расшифровки данных по 'Исходному средству' из data_collection.

        :param data: словарь со всеми данными (включая подробную инфу по продуктам)
        :param data_collection: словарь с подборкой (где есть ключ 'Исходное средство')
        :param category: категория, с которой работаем
        :return: строка с подробной информацией по исходному средству
        """

        # Получаем название исходного средства из data_collection
        origin_product_name = data_collection.get("Исходное средство")

        origin_product_data = data.get(category, {}).get(origin_product_name, {})

        # Формируем словарь с информацией о средстве
        origin_product_full_info = {
            origin_product_name: {
                "Тип продукта": origin_product_data.get("Тип продукта", "Не указан"),
                "Состав": origin_product_data.get("Состав", "Не указан")
            }
        }

        # Возвращаем результат, преобразованный в строку

        # Достаём значения
        product_info = origin_product_full_info[origin_product_name]

        result_string = (
            f"Название средства: {origin_product_name}. "
            f"Тип продукта: {product_info['Тип продукта']}. "
            f"Состав: {product_info['Состав']}. "
        )

        return result_string

    def _format_pairs_for_prompt(
            self,
            pairs: dict) -> str:
        """
        Метод, работающий для кода задачи "Лучшая пара", форматирует
        пары средств в читаемую строку для промпта.
        """
        output = ""
        for pair_name, products in pairs.items():
            output += f"\n{pair_name}:\n"
            for product_name, product_info in products.items():
                output += f"- Продукт: {product_name}\n"
                output += f"  Тип продукта: {product_info.get('Тип продукта', 'Не указан')}\n"
                output += f"  Состав: {product_info.get('Состав', 'Не указан')}\n"
        return output

    def decrypting_best_pair(
            self,
            data: dict,
            data_collection: dict,
            category: str,
    ) -> dict:
        """
        Метод для расшифровки ключа средства для кода задачи "Лучшая пара".
        :param data: словарь со всеми данными по средствам
        :param data_collection: словарь с подборкой пар
        :param category: категория, с которой работаем
        :return: словарь с расшифрованными данными по каждой паре
        """

        # Получаем пары из подборки
        pairs = data_collection.get(category, {})

        # Сюда сохраняем результат
        result = {}

        # Проходим по всем парам
        for pair_key, product_list in pairs.items():
            pair_info = {}

            for product_name in product_list:
                product_data = data.get(category, {}).get(product_name, {})

                pair_info[product_name] = {
                    "Тип продукта": product_data.get("Тип продукта", "Не указан"),
                    "Состав": product_data.get("Состав", "Не указан"),
                }

            result[pair_key] = pair_info

        new_result = self._format_pairs_for_prompt(pairs=result)

        return new_result

    def main_decryp_data_from_current_collection(
            self,
            data_tools: dict,
            data_collection: dict,
    ) -> dict:
        """
        Функция для расшифровки данных из словаря текущей подборки

        :param data_tools: словарь с информацией о средствах, типах и прочем
        :param data_collection: словарь с данными текущей подборки
        :return: словарь с расшифрованными данными по текущей подборке
        """

        # расшифровка средств в зависимости от задачи
        function_for_decryption_products = self.method_for_task_code[data_collection["Задача"]]

        if data_collection["Задача"] == "Лучшая пара":
            data_collection["Средства"] = function_for_decryption_products(
                data=data_tools,
                data_collection=data_collection,
                category="Средства",
            )
        else:
            data_collection["Средства"] = function_for_decryption_products(
                data=data_tools,
                data_collection=data_collection,
                category="Средства",
            )

        if "Исходное средство" in data_collection:
            data_collection["Исходное средство"] = self.decrypting_origin_product_info(
                data=data_tools,
                data_collection=data_collection,
                category="Средства",
            )

        # расшифровка данных по ключу Тип
        data_collection['Тип'] = self._decrypting_data_from_cell(
            data=data_tools,
            data_collection=data_collection,
            category="Тип",
        )

        # расшифровка данных по ключу Запрос
        data_collection["Запрос"] = self._decrypting_data_from_cell(
            data=data_tools,
            data_collection=data_collection,
            category="Запрос",
        )

        # расшифровка данных по ключу Задача - ее содержимое пойдет в settings
        data_collection["Задача"] = self._decrypting_info_from_cell(
            data=data_tools,
            data_collection=data_collection,
            category="Задача",
        )

        # расшифровка данных по ключу Специалист - ее содержимое пойдет в system
        data_collection["Специалист"] = self._decrypting_info_from_cell(
            data=data_tools,
            data_collection=data_collection,
            category="Специалист",
        )

        return data_collection
