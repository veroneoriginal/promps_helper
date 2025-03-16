class PromptConstructor:
    """
    Класс для создания промптов для отправки в контекст
    """

    def construct_prompt_for_best_product(
            self,
            data_collection: dict,
    ) -> dict:
        """
        Метод для формирования текстового промпта на основе
        данных словаря для кода "Лучшее средство".

        :param data_collection: словарь с расшифрованными данными по текущей подборке
        :return: словарь с системным промптом и основным промптом за отправки запроса.
        """

        return {
            'system_prompt': f"{data_collection['Специалист']}",
            'prompt': f"""
Подборка осуществляется для человека, который имеет {data_collection["Пол"]} пол,
возраст: {data_collection["Возраст"]} года/лет.
Так же у человека следующие параметры: {data_collection['Тип']}.
С помощью подбираемого средства человек хочет решить следующую проблему:
{data_collection['Запрос']}.

Информация о средствах, их типе и составах:
{data_collection["Средства"]}.

Учти всю вышепредставленную информацию и проведи анализ составов.

Ответ ты должен дать в следующем виде: {data_collection['Задача']}"""
        }

    def construct_prompt_for_one_product(
            self,
            data_collection: dict,
    ) -> dict:
        """
        Метод для формирования текстового промпта на основе данных словаря
        для кода 'Разбор состава одного средства'.

        :param data_collection: словарь с расшифрованными данными по текущей подборке
        :return: словарь с системным промптом и основным промптом за отправки запроса.
        """

        return {
            'system_prompt': f"{data_collection['Специалист']}",
            'prompt': f"""
Подборка осуществляется для человека, который имеет {data_collection["Пол"]} пол,
возраст: {data_collection["Возраст"]} года/лет.
Так же у человека следующие параметры: {data_collection['Тип']}.
С помощью этого средства человек хочет решить следующую проблему:
{data_collection['Запрос']}.

Информация о средстве и его составе: {data_collection["Средства"]}.

Учти всю вышепредставленную информацию и проведи детальный анализ состава.

Ответ ты должен дать в следующем виде: {data_collection['Задача']}"""
        }

    def main_constructor_prompt(
            self,
            data: dict,
            data_collection: dict,
    ) -> dict:
        """
        Главная функция класса, которая определяет какой промпт будет отправлен в OpenAI.

        :param data: словарь с информацией для выбора промпта
        :param data_collection: словарь с расшифрованными данными по текущей подборке
        :return: dict
        """

        prompts = {
            'Лучшее средство': self.construct_prompt_for_best_product,
            'Лучшее средство без канцерогенов': self.construct_prompt_for_best_product,
            'Разбор состава одного средства': self.construct_prompt_for_one_product,
        }

        task = data["Задача"]
        return prompts[task](data_collection=data_collection)
