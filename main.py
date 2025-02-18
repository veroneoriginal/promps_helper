"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
from datetime import datetime
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
from appeal_to_openai.main import main as appeal_to_openai_main
from appeal_to_openai.utils import checking_file_with_response
from excel_process_data.main import main as load_data_main
from excel_process_data.process_data import ExcelManager
from pdf.main_pdf import PDFCreator
from pdf.utils import forming_indo_for_pdf
from post_constructor.post_constructor import create_text_for_post
from prompt_constructor.constructor import PromptConstructor
from prompt_constructor.json_schemes.json_schemes import determine_scheme_by_number_of_products
from prompt_constructor.settings_constructor.settings_response import SETTINGS_RESPONSE
from prompt_constructor.settings_constructor.system_prompt import SYSTEM_PROMPT


class ControlManager:
    """
    Класс, управляющий логикой весго проекта
    """
    def __init__(self):
        self.output_paths = {}

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
        1_Шампуни) созданию готового контекста, который передается в OpenAI,
        2_Масла) отправке самого запроса в OpenAI,
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
        Функция для создания словаря со всей информацией по средствам из нужной подборки

        :param file_path: путь до документа .xlsx
        :return: словарь с всеми данными по средствам
        """

        instance_excel = ExcelManager(file_path=file_path)

        # формирование словаря из листа "Подборки" с нужными средствами
        collection_dict = instance_excel.forming_dict_from_collection(ws_title='Подборки')

        # дополненный всей информацией о средствах словарь из листа "Средства"
        return instance_excel.add_data_from_the_tools_page(
            ws_title='Средства',
            data=collection_dict,
        )

    def _get_output_folders(
            self,
            path_to_output_folder: str,
            category: str,
    ) -> dict:
        """
        Создает папки для сохранения файлов и возвращает их пути.

        :param category: название категории для подпапки.
        :param path_to_output_folder: путь до основной папки, в которую идет сохранение.
        """

        # Получаем текущую дату в формате ДД_ММ_ГГ
        timestamp = datetime.now().strftime("%d_%m_%y")

        # Определяем базовую папку
        base_output_folder = Path(path_to_output_folder) / timestamp
        base_output_folder.mkdir(parents=True, exist_ok=True)

        # Получаем список существующих папок в базовой директории
        existing_folders = []
        for d in base_output_folder.iterdir():
            if d.is_dir():
                existing_folders.append(d)

        # Определяем новый номер папки
        new_folder_number = 1
        if existing_folders:
            last_number = 0
            for folder in existing_folders:
                parts = folder.name.split('_')
                if parts[0].isdigit():
                    last_number = max(last_number, int(parts[0]))
            new_folder_number = last_number + 1

        # Формируем имя новой папки
        category_folder_name = f"{new_folder_number}_{category}"
        category_folder = base_output_folder / category_folder_name
        category_folder.mkdir(exist_ok=True)

        # Создаем основные папки
        subfolders = ["instagram", "telegram", "pinterest"]

        for subfolder in subfolders:
            subfolder_path = category_folder / subfolder
            subfolder_path.mkdir(exist_ok=True)
            self.output_paths[subfolder] = str(subfolder_path)

            # Если это telegram, создаем вложенные папки
            if subfolder == "telegram":
                telegram_subfolders = ["text", "pdf", "jpg"]
                for t_subfolder in telegram_subfolders:
                    t_subfolder_path = subfolder_path / t_subfolder
                    t_subfolder_path.mkdir(exist_ok=True)
                    self.output_paths[f"telegram_{t_subfolder}"] = str(t_subfolder_path)

        return self.output_paths

    def _create_pdf_jpg_for_post(
            self,
            info_for_picture: dict,
            path_to_output_folder: str,

    ) -> None:
        """
        Метод для создания pdf-листов в телеграм (для постов со средствами)

        :param info_for_picture: словарь со всеми данными по средствам
        :return: None
        """
        # из огромного словаря со всеми данными, берем инфу для картинки в пост
        list_with_info = forming_indo_for_pdf(data=info_for_picture)

        # Получаем пути для сохранения файлов
        folders = self._get_output_folders(path_to_output_folder=path_to_output_folder)

        create_pdf = PDFCreator()
        create_pdf.gen_pages_for_six_product(
            list_with_info=list_with_info,
            # Формируем путь для output_folder
            output_folder_pdf=folders["pdf"],
            output_folder_jpg=folders["jpg"],
        )

    def _forming_text_for_post(
            self,
            data: dict,
            info_for_picture: dict,
            path_to_output_folder: str,
    ):
        """В эту функцию приходит промпт, и словарь, соединяю все воедино и возвращаю строку"""

        full_info = create_text_for_post(
            data=data,
            info_for_picture=info_for_picture
        )

        path_to_file = self.output_paths["telegram_text"]

        # Получаем пути для сохранения файлов
        output_file = path_to_file / "text_for_post.md"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(full_info)

    def create_collection(
            self,
            category: str,
            path_to_output_folder: str,
            json_file_path: str,
            product_count: int = 6 | 4,
    ) -> None:
        """
        Главный метод класса, в котором собрана вся логика программы

        :param category: категория, по которйо осуществляется по подборка

        :param json_file_path: путь до json-файла
        :param product_count: количество средств, которые анализируюся
        :param path_to_output_folder: путь до папки, в которую идет сохранение.
        :return: None
        """

        # Исходя из категории, формируем путь до документа .xlsx
        file_path = f'00_base/{category}.xlsx'

        # print('Определяю json-схему.')
        # json_scheme = self._determine_scheme_for_response_format(product_count=product_count)
        #
        # print('Забираю данные из таблицы.')
        # data = self._take_data_from_the_table(file_path=file_path)
        #
        # print('Собираю промпт.')
        # prompt = self._bring_prompt(dict_with_info=data)
        #
        # print('Отправляю запрос в OpenAI.')
        # self._create_context_for_request_to_openai(prompt_for_convert=prompt,
        #                                            json_scheme=json_scheme)
        #
        # print('Разбираю ответ от OpenAI.')
        # self._reviewing_response_from_openai(file_path=file_path,
        #                                      json_file_path=json_file_path)
        #
        # print('Формируем данные для картинок.')
        # info_for_picture = self._generating_data_for_images(file_path=file_path)

        print('Формируем пути сохранения данных.')
        self._get_output_folders(path_to_output_folder=path_to_output_folder,
                                 category=category)

        # print('Готовим текстовое оформление поста.')
        # self._forming_text_for_post(data=data, info_for_picture=info_for_picture,
        #                             path_to_output_folder=path_to_output_folder)

        # print('Создаю изображения со средствами для Telegram-поста.')
        # self._create_pdf_jpg_for_post(
        #     info_for_picture=info_for_picture,
        #     path_to_output_folder=path_to_output_folder,
        # )



if __name__ == '__main__':
    instance = ControlManager()
    instance.create_collection(
        category="Маски",
        json_file_path='00_base/prompt/history_prompt/Анализ_средств.json',
        product_count=6,
        path_to_output_folder='00_base/00_info_for_post/',
    )
