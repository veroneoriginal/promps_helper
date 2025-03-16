class PDFDataProcessor:
    """
    Класс для подготовки данных к передаче в PDFCreator
    """

    def __init__(
            self,
            collection_data: dict,
            info_data: dict,
            selection_result: dict,
            path_to_output_folder: str,

    ) -> None:
        """
        :param collection_data: данные подборки
        :info_data: данные с всеми средствами, врачами и т.д.
        :selection_result: данные с результатом нейронки по подборке
        :param path_to_output_folder: пути для сохранения
        :return: None
        """

        self.collection_data = collection_data
        self.info_data = info_data
        self.selection_result = selection_result
        self.path_to_output_folder = path_to_output_folder

        self.method_for_task_code = {
            'Лучшее средство': self._best_product,
            'Лучшее средство без канцерогенов': self._best_product_without_carcinogens,
            'Разбор состава одного средства': self._analysis_composition_one_product,
            'Лучшая пара': self._best_para,
            'Лучшее сочетание': self._best_combination,
            'Лучшая компоновка': self._best_layout,
            'Аналог': self._analogue,
            'Наиболее похож': self._most_similar,
            'Наименее похож': self._least_similar,
        }

    def process_data_with_task_code(self):
        """
        Вызывает нужную логику в зависимости от кода задачи
        """

        task = self.collection_data['Задача']
        self.method_for_task_code[task]()



    def _least_similar(self):
        """ Наименее похож """
        pass

    def _most_similar(self):
        """ Наиболее похож """
        pass

    def _analogue(self):
        """ Аналог """
        pass

    def _best_layout(self):
        """ Лучшая компоновка """
        pass

    def _best_combination(self):
        """ Лучшее сочетание """
        pass

    def _best_para(self):
        """ Лучшая пара """
        pass

    def _analysis_composition_one_product(self):
        """
        Разбор состава одного средства
        """
        pass

    def _best_product_without_carcinogens(self):
        """
        Лучшее средство без канцерогенов
        """
        pass

    def _best_product(self):
        """
        Лучшее средство
        """
        pass




