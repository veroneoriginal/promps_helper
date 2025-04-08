class PromptConstructor:
    """
    Класс для создания промптов для отправки в контекст
    """

    def __init__(self):
        self.prompts = {
            'Лучшее средство': self.products_for_code_best_product,
            'Лучшее средство без канцерогенов':
                self.products_for_code_best_product_carcinogen_free,
            'Разбор состава одного средства': self.products_for_code_one_product,
            'Лучшая пара': self.products_for_code_best_couple,
            'Лучшее сочетание': self.products_for_code_best_combination,
            'Лучшая компоновка': 'метод который расшифровывает словарь для этого кода задачи',
            'Аналог': self.products_for_code_analogue_product,
            'Наиболее похож': 'метод который расшифровывает словарь для этого кода задачи',
            'Наименее похож': 'метод который расшифровывает словарь для этого кода задачи',
        }

    def create_prompt_with_user_parameters(
            self,
            data_decrypted: dict,
            task: dict,
    ) -> dict:
        """
        Метод для формирования текстового промпта для отправки в OPENAI с учётом
        параметров пользователя

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :param task: строка с кодом задачи по текущей подборке
        :return: словарь с системным промптом и основным промптом за отправки запроса.
        """

        return {
            'system_prompt': f"{data_decrypted['Специалист']}",
            'prompt': f"""
Подборка осуществляется для человека, который имеет {data_decrypted["Пол"]} пол,
возраст: {data_decrypted["Возраст"]} года/лет.
Так же у человека следующие параметры: {data_decrypted['Тип']}.
С помощью подбираемого средства человек хочет решить следующую проблему:
{data_decrypted['Запрос']}.

{self.prompts[task](data_decrypted=data_decrypted)}

Ответ ты должен дать в следующем виде: {data_decrypted['Задача']}"""
        }

    def create_prompt_without_user_parameters(
            self,
            data_decrypted: dict,
            task: dict,
    ) -> dict:
        """
        Метод для формирования текстового промпта для отправки в OPENAI БЕЗ учёта
        параметров пользователя

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :param task: строка с кодом задачи по текущей подборке
        :return: словарь с системным промптом и основным промптом за отправки запроса.
        """


        return {
            'system_prompt': f"{data_decrypted['Специалист']}",
            'prompt': f"""{self.prompts[task](data_decrypted=data_decrypted)}
    Ответ ты должен дать в следующем виде: {data_decrypted['Задача']}"""
        }

    def products_for_code_analogue_product(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового описания блока со средствами
        для кода "Аналог".

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
       :return: строка с описанием средств
        """

        return f"""
Информация о средствах, их типе и составах: {data_decrypted["Средства"]}.
Учти всю вышепредставленную информацию и сделай вывод.
"""

    def products_for_code_best_product(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового описания блока со средствами
        для кода "Лучшее средство".

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
       :return: строка с описанием средств
        """

        return f"""
Информация о средствах, их типе и составах: {data_decrypted["Средства"]}.
Учти всю вышепредставленную информацию и проведи анализ составов.
"""

    def products_for_code_best_product_carcinogen_free(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового описания блока со средствами
        для кода "Лучшее средство без канцирогенов".

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :return: строка с описанием средств
        """

        return f"""
Информация о средствах, их типе и составах: {data_decrypted["Средства"]}.

Учти всю вышепредставленную информацию и проведи анализ составов.
Если в составе есть канцерогены, то укажи их названия. Максимально внимательно проверь составы на наличие канцерогенов, это очень важно.
"""

    def products_for_code_one_product(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового описания блока со средствами
        для кода 'Разбор состава одного средства'.

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :return: строка с описанием средств
        """

        return f"""
Информация о средстве и его составе: {data_decrypted["Средства"]}.
Учти всю вышепредставленную информацию и проведи детальный анализ состава.
"""

    def products_for_code_best_couple(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового промпта на основе данных словаря
        для кода 'Лучшая пара'.

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :return: строка с описанием средств
        """

        return f"""
Информация о наборах средств:{data_decrypted["Средства"]}.
Учти всю вышепредставленную информацию и выдели лучший набор из представленных. 
"""

    def products_for_code_best_combination(
            self,
            data_decrypted: dict,
    ) -> str:
        """
        Метод для формирования текстового описания блока со средствами
        для кода 'Лучшее сочетание'.

        :param data_decrypted: словарь с расшифрованными данными по текущей подборке
        :return: строка с описанием средств
        """

        return f"""
Информация об исходном средстве, к которому подбираем дополнение, и его состав,
а так же информация о средствах, которые подбираем к исходному средству,
и их составах представлены далее: {data_decrypted["Средства"]}.

Учти всю вышепредставленную информацию и подбери наиболее подходящее одно средство в дополнение к исходному. 
"""

    def main_constructor_prompt(
            self,
            data_decrypted: dict,
            task: dict,
    ) -> dict:
        """
        Главная функция класса, которая определяет какой промпт будет отправлен в OpenAI.

        :param data_decrypted: расшифрованный словарь с данными по текущей подборке
        :param task: строка с кодом задачи по текущей подборке
        :return: словарь с промптом
        """

        if data_decrypted['Параметры'].strip().lower() == 'учитывать':

            return self.create_prompt_with_user_parameters(
                data_decrypted=data_decrypted,
                task=task,
            )
        return self.create_prompt_without_user_parameters(
            data_decrypted=data_decrypted,
            task=task,
        )
