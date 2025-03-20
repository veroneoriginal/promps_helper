class JsonProcessingData:
    """
    Класс, внутри которого расшифровываются данные только категории 'Средства'
    текущей подборки в зависимости от кода задачи.

    :param data_collection: данные подборки
    :return: расшифрованный словарь текущей подборки
    """

    def __init__(
            self,
            data_collection: dict,
    ):
        self.data_collection = data_collection
        self.method_for_task_code = {
            'Лучшее средство': self.decryption_task_best_product,
            'Лучшее средство без канцерогенов': self.decryption_task_best_product,
            'Разбор состава одного средства': self.decryption_task_one_product,
            'Лучшая пара': 'метод который расшифровывает словарь для этого кода задачи',
            'Лучшее сочетание': self.decryption_task_best_combination,
            'Лучшая компоновка': 'метод который расшифровывает словарь для этого кода задачи',
            'Аналог': 'метод который расшифровывает словарь для этого кода задачи',
            'Наиболее похож': 'метод который расшифровывает словарь для этого кода задачи',
            'Наименее похож': 'метод который расшифровывает словарь для этого кода задачи',
        }

    def distribution_on_task(self):
        """
        С помощью этого метода определяю какую функцию для расшифровки вызывать
        """
        task = self.data_collection['Задача']
        result_function = self.method_for_task_code[task]
        return result_function(self.data_collection)

    def decryption_task_best_product(
            self,
            data_collection: dict,
    ) -> dict:
        """
        Метод для преобразования словаря по коду задачи - 'Лучшее средство'.
        Считаем длину словаря по ключу 'Средства' и обновляем исходный словарь.

        :param data_collection: словарь с текущей подборкой
        :return: словарь с текущей подборкой с добавленным ключом 'Количество средств'
        """

        data_collection['Количество средств'] = len(data_collection['Средства'])

        return data_collection

    def decryption_task_one_product(
            self,
            data_collection: dict,
    ) -> dict:
        """
        Функция для преобразования словаря по коду задачи - 'Разбор состава одного средства'.

        :param data_collection: словарь с текущей подборкой
        :return: тот же самый словарь без изменений
        """

        return data_collection

    def decryption_task_best_combination(
            self,
            data_collection: dict,
    ) -> dict:
        """
        Метод для преобразования словаря по коду задачи - 'Лучшее сочетание'.
        Выносим исходное средство в отдельный ключ, потому что оно всегда будет одно.
        Затем обновляем исходный словарь, чтобы в ключе средства были только средства,
        которые подбираются к исходному, т.к. их число может меняться.

        :param data_collection: словарь с текущей подборкой
        :return: словарь с текущей подборкой добавленным ключом 'Исходное средство'
        """

        data_collection['Исходное средство'] = data_collection['Средства'].pop('Исходное средство')
        data_collection['Количество средств'] = len(data_collection['Средства'])

        return data_collection
