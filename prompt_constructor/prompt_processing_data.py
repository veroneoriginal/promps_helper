from dotenv.variables import Literal


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
            'Разбор состава одного средства': self.decrypting_info_code_best_product,
            'Лучший набор': self.decrypting_best_set,
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

        # Убираем лишние пробелы с начала и конца строки
        type_need = type_of_need.strip()

        # Проверяем, есть ли символ в строке
        if symbol in type_need:
            # Если есть символ, разделяем и очищаем значения
            values = type_need.split(symbol)
            return [value.strip() for value in values]

        # Если символа нет, возвращаем список с одним очищенным значением
        return [type_need.strip()]

    def _decrypting_data_from_cell(
            self,
            data: dict,
            data_collection: dict,
            key_for_decrypted: str,
    ) -> str:
        """
        Метод для расшифровки данных из блоков Тип, Запрос

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param key_for_decrypted: категория, с который работаем
        :return: расшифрованная строка
        """

        # получение строки с содержимым, которое было в ячейке ТИП
        body_part_type = data_collection[key_for_decrypted]

        # формирование из строки списка отдельных элементов
        list_body_part_type = self._split_and_clean_type(
            type_of_need=body_part_type,
            symbol=",",
        )

        # формирование списка словарей с расшифрованными значениями
        params = []

        # расшифровывание кодов и добавление в этот новый список
        for element in list_body_part_type:
            params.append(data[key_for_decrypted][element])

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
            key_for_decrypted: str,
    ) -> str:
        """
        Метод для расшифровки данных из блоков Задача, Специалист

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param key_for_decrypted: категория, с который работаем
        :return: расшифрованная строка
        """

        # получение строки с содержимым, которое было в ячейке
        body_part_type = data_collection[key_for_decrypted]

        # обращение по полученному коду к основному словарю с содержимым
        dict_with_full_info = data[key_for_decrypted][body_part_type]

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
                f"{value['Номер']} - {key}. "
                f"Состав: {value['Состав']}. Тип продукта: {value['Тип продукта']}. ")

        # строка, которая объединяет инфо о всех сред-х в единый текст блок с переносами строк
        return "\n".join(list_cosmetic_products)

    def decryped_dict_with_one_product(
            self,
            data: dict,
            product_name: str,
            list_name: Literal = 'Средства',
    ) -> dict:
        """
        Метод для создания словаря с расшифрованным средством

        :param data: база данных
        :param product_name: название средства
        :param list_name: название листа из базы данных со средствами

        :return: словарь с расшифрованным средством
        """

        product_data = data[list_name][product_name]

        return {
            "Тип продукта": product_data.get("Тип продукта", "Не указан"),
            "Состав": product_data.get("Состав", "Не указан"),
        }

    def decryption_product_current_collection(
            self,
            data: dict,
            products: dict,
    ) -> dict:
        """
        Метод, с помощью которого расшифровываем словарь со средствами из текущй подборки

        :param data: словарь со всеми данными
        :param products: словарь из ключа Средства из текущей подборки

        :return: расшифрованный словарь со средствами
        """
        # формируем словарь
        formated_products = {}

        for product_key, product_name in products.items():
            # ищем данные по product_name в основном data словаре
            formated_products[product_name] = self.decryped_dict_with_one_product(
                data=data,
                product_name=product_name,
            )

            formated_products[product_name]["Номер"] = product_key

        return formated_products

    def decrypting_info_code_best_product(
            self,
            data: dict,
            data_collection: dict,
            key_for_decrypted: str,
    ) -> str:
        """
        Метод для расшифровки данных из блока Средства для кода задачи
        'Лучшее средство', 'Лучшее средство без канцерогенов', 'Лучшее сочетание'

        :param data: словарь со всеми данными
        :param data_collection: словарь с подборкой
        :param key_for_decrypted: категория, с которой работаем
        :return: словарь со средствами, их типом и составом
        """

        # получение словаря из ключа Средства из текущей подборки
        products: dict = data_collection[key_for_decrypted]

        formated_products = self.decryption_product_current_collection(
            data=data,
            products=products,
        )
        # преобразование словаря со средствами в строку
        return self._conversion_products(cosmetic_products=formated_products)

    def decrypting_origin_product_info(
            self,
            data: dict,
            data_collection: dict,
            key_for_decrypted: str,
    ) -> str:
        """
        Метод для расшифровки данных по 'Исходному средству' из data_collection.

        :param data: словарь со всеми данными (включая подробную инфу по продуктам)
        :param data_collection: словарь с подборкой (где есть ключ 'Исходное средство')
        :param key_for_decrypted: категория, с которой работаем
        :return: строка с подробной информацией по исходному средству
        """

        # Получаем название исходного средства из data_collection
        origin_product_name = data_collection.get("Исходное средство")

        origin_product_data = data.get(key_for_decrypted, {}).get(origin_product_name, {})

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

    def _format_set_for_prompt(
            self,
            product_set: dict,
    ) -> str:
        """
        Метод, работающий для кода задачи "Лучший набор", форматирует наборы
        средств в читаемую строку для промпта.

        :param product_set: набор из средств (пара, тройка, четверка средств)
        :return: набор средств преобразованный из словаря в строку
        """
        lines = []

        for product_group_name, products in product_set.items():
            lines.append(f"\n{product_group_name}:")
            for product_name, product_info in products.items():
                lines.append(f"Продукт: {product_name}. "
                             f"Тип продукта: {product_info.get('Тип продукта', 'Не указан')}. "
                             f"Состав: {product_info.get('Состав', 'Не указан')}. ")

        return "\n".join(lines)

    def decrypting_best_set(
            self,
            data: dict,
            data_collection: dict,
            key_for_decrypted: str,
    ) -> str:
        """
        Метод для расшифровки ключа средства для кода задачи 'Лучший набор'.

        :param data: словарь со всеми данными по средствам
        :param data_collection: словарь с подборкой наборов
        :param key_for_decrypted: категория, с которой работаем
        :return: строка с расшифрованными данными по каждой паре
        """

        # получение словаря из ключа Средства из текущей подборки
        products: dict = data_collection[key_for_decrypted]

        # Сюда сохраняем результат
        group_products = {}

        # Проходим по всем группам
        for product_group_name, product_dict in products.items():

            formated_products = self.decryption_product_current_collection(
                data=data,
                products=product_dict,
            )

            group_products[product_group_name] = formated_products

        return self._format_set_for_prompt(product_set=group_products)

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

        data_collection["Средства"] = function_for_decryption_products(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted="Средства",
        )

        # расшифровка данных по ключу Тип
        data_collection['Тип'] = self._decrypting_data_from_cell(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted="Тип",
        )

        # расшифровка данных по ключу Запрос
        data_collection["Запрос"] = self._decrypting_data_from_cell(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted="Запрос",
        )

        # расшифровка данных по ключу Задача - ее содержимое пойдет в settings
        data_collection["Задача"] = self._decrypting_info_from_cell(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted="Задача",
        )

        # расшифровка данных по ключу Специалист - ее содержимое пойдет в system
        data_collection["Специалист"] = self._decrypting_info_from_cell(
            data=data_tools,
            data_collection=data_collection,
            key_for_decrypted="Специалист",
        )

        return data_collection
