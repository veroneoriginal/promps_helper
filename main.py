"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
from pprint import pprint

from dotenv import load_dotenv

from appeal_to_openai.main import main as appeal_to_openai_main
from appeal_to_openai.utils import checking_file_with_response
from excel_process_data.main import main as load_data_main
from excel_process_data.process_data import ExcelManager
from excel_process_data.utils.utils import creating_dict_for_pdf
from prompt_constructor.constructor import PromptConstructor
from prompt_constructor.json_schemes.json_schemes import determine_scheme_by_number_of_products
from prompt_constructor.settings_constructor.settings_response import SETTINGS_RESPONSE
from prompt_constructor.settings_constructor.system_prompt import SYSTEM_PROMPT


class ControlManager:
    """
    Класс, управляющий логикой весго проекта
    """

    def _take_data_from_the_table(
            self,
            file_path: str,
    ) -> dict:
        """
        Функция для загрузки данных из таблицы

        :param file_path: путь до документа .xlsx
        :return: словарь с описанием параметров пользователя и средствами для анализа
        """

        return load_data_main(file_path=file_path)

    def _bring_prompt(
            self,
            dict_with_info: dict,
    ) -> str:
        """
        В этой функции осуществляется вызов функции для создания промпта

        :param dict_with_info: словарь с описанием параметров пользователя и средствами для анализа
        :return: промпт в виде строки
        """

        instance_create_prompt = PromptConstructor()
        return instance_create_prompt.construct_prompt(
            data=dict_with_info,
            settings_response=SETTINGS_RESPONSE,
        )

    def _create_context_for_request_to_openai(
            self,
            prompt_for_convert: str,
            json_scheme: dict,
    ) -> None:
        """
        В этой функции осуществляется вызов ключевой функции по:
        1) созданию готового контекста, который передается в OpenAI,
        2) отправке самого запроса в OpenAI,
        3) сохранение результата

        :param prompt_for_convert: промпт для преобразования его в контекст
        :return: None
        """

        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')

        appeal_to_openai_main(
            prompt=prompt_for_convert,
            system_prompt=SYSTEM_PROMPT,
            api_key=openai_api_key,
            json_scheme=json_scheme,
        )

    def _reviewing_response_from_openai(
            self,
            file_path: str,
            json_file_path: str,
    ) -> None:
        """
        В этой функции разбираю ответ от OpenAI.

        :param file_path: путь до документа .xlsx
        :param json_file_path: путь до json-файла

        :return: None
        """

        data = checking_file_with_response(json_file_path=json_file_path)

        instance_excel = ExcelManager(file_path=file_path)

        instance_excel.writing_data_from_json_to_excel(data=data)

    def _determine_scheme_for_response_format(
            self,
            product_count: int = 6 | 4,
    ) -> dict:
        """
        Функция для вызова полной функции по выбору json-scheme.

        :param product_count: количество средств, которые анализируюся
        :return: json-scheme в виде словаря
        """

        return determine_scheme_by_number_of_products(product_count=product_count)

    def _generating_data_for_images(
            self,
            file_path: str,
    ) -> dict:
        """
        Функция для создания словаря со всей информацией по средствам
        из нужной подборки для вставки в картинку

        :param file_path: путь до документа .xlsx
        :return: словарь с данными по средствам для вставки в картинку
        """

        instance_excel = ExcelManager(file_path=file_path)

        # формирование словаря из листа "Подборки"
        collection_dict = instance_excel.forming_dict_from_collection(ws_title='Подборки')

        # дополнение словаря всей информацией из листа "Средства"
        full_dict = instance_excel.add_data_from_the_tools_page(
            ws_title='Средства',
            data=collection_dict,
        )

        # формирование словаря только с теми параметрами,
        # которые нужны для вставки в картинку
        return creating_dict_for_pdf(dict_full_info=full_dict)

    def create_collection(
            self,
            file_path: str,
            json_file_path: str,
            product_count: int = 6 | 4,
    ) -> None:
        """
        Главный метод класса, в котором собрана вся логика программы

        :param file_path: путь до документа .xlsx
        :param json_file_path: путь до json-файла
        :param product_count: количество средств, которые анализируюся
        :return: None
        """

        print('Определяю json-схему.')
        json_scheme = self._determine_scheme_for_response_format(product_count=product_count)

        print('Забираю данные из таблицы.')
        data = self._take_data_from_the_table(file_path=file_path)

        print('Собираю промпт.')
        prompt = self._bring_prompt(dict_with_info=data)

        print('Отправляю запрос в OpenAI.')
        self._create_context_for_request_to_openai(prompt_for_convert=prompt,
                                                   json_scheme=json_scheme)

        print('Разбираю ответ от OpenAI.')
        self._reviewing_response_from_openai(file_path=file_path,
                                             json_file_path=json_file_path)

        print('Формируем данные для картинок.')
        info_for_picture = self._generating_data_for_images(file_path=file_path)
        pprint(info_for_picture)

        print('Следующий шаг - создание изображений со средствами.')



if __name__ == '__main__':
    instance = ControlManager()
    instance.create_collection(
        file_path='00_base/00_Средства.xlsx',
        json_file_path="prompt/history_prompt/Анализ_средств.json",
        product_count=6,
    )
