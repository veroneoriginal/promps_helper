"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
from dotenv import load_dotenv


from appeal_to_openai.main import main as appeal_to_openai_main
from load_data.main import main as load_data_main
from prompt_constructor.constructor import PromptConstructor
from prompt_constructor.settings_constructor.settings_response import SETTINGS_RESPONSE
from prompt_constructor.settings_constructor.system_prompt import SYSTEM_PROMPT



class ControlManager:
    """
    Класс, управляющий логикой весго проекта
    """

    def take_data_from_the_table(
            self,
            file_path,
    ) -> dict:
        """
        Функция для загрузки данных из таблицы

        :param file_path: путь до документа .xlsx
        :return: словарь с описанием параметров пользователя и средствами для анализа
        """

        return load_data_main(file_path=file_path)

    def bring_prompt(
            self,
            data: dict,
    ) -> str:
        """
        В этой функции осуществляется вызов функции для создания промпта

        :param data: словарь с описанием параметров пользователя и средствами для анализа
        :return: промпт в виде строки
        """

        instance_create_prompt = PromptConstructor()
        return instance_create_prompt.construct_prompt(
            data=data,
            settings_response=SETTINGS_RESPONSE,
        )

    def create_context_for_request_to_openai(
            self,
            prompt: str,
    ) -> None:
        """
        В этой функции осуществляется вызов ключевой функции по:
        1) созданию готового контекста, который передается в OpenAI,
        2) отправке самого запроса в OpenAI,
        3) сохранение результата

        :param prompt: промпт для преобразования его в контекст
        :return: None
        """

        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')

        appeal_to_openai_main(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            api_key=openai_api_key,
        )


if __name__ == '__main__':
    instance = ControlManager()

    print('Забираю данные из таблицы')
    data = instance.take_data_from_the_table(file_path='../00_base/00_Средства.xlsx')

    print('Собираю промпт.')
    prompt = instance.bring_prompt(data=data)

    print('Отправляю запрос в OpenAI.')
    instance.create_context_for_request_to_openai(prompt=prompt)

    # print('Разбираю ответ от OpenAI.')
    #
    # print('Готовлю изображения со средствами.')
