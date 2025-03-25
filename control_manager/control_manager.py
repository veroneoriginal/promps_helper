
"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
from pathlib import Path

# from pprint import pprint

from dotenv import load_dotenv
from appeal_to_openai.main import main as appeal_to_openai_main
from appeal_to_openai.utils import checking_file_with_response
from dirs_structure_constructor.main import DirsConstructor
from excel_process_data.process_data import ExcelManager
from pdf.main import create_pdf
from post_constructor.post_constructor import create_text_for_post
from json_constructor.main import get_json_scheme
from prompt_constructor.main import get_prompt

# from utils.utils import (
#     copy_jpg_files,
#     transforming_dict_from_json_file,
#     add_keys_from_another_dict_to_one_dict,
# )


class ControlManager:
    """
    Класс, управляющий логикой всего проекта
    """

    def __init__(self, param_dif_products_categories):
        """
        :param param_dif_products_categories: особенности для подборок, учитываются в промптах
        """
        self.paths_to_folders = {}
        self.param_dif_products_categories = param_dif_products_categories

    def _take_data_from_table_tool(
            self,
            file_path_tools_table: str,
    ) -> dict:
        """
        Метод для загрузки всех данных из таблицы Средства.

        :param file_path_tools_table: путь до документа Средства.xlsx
        :return: словарь с информацией о средствах, типах, запросе, задаче, специалистах
        """

        excel_manager = ExcelManager(file_path=file_path_tools_table)

        return {
            "Средства": excel_manager.load_info_about_products(ws_title='Средства'),
            "Тип": excel_manager.load_type_data(ws_title='Тип'),
            "Запрос": excel_manager.load_user_request(ws_title='Запрос'),
            "Задача": excel_manager.load_tasks_data(ws_title='Задача'),
            "Специалист": excel_manager.load_specialists_data(ws_title='Специалист'),
        }

    def _get_count_collections(
            self,
            file_path_collection: str,
    ) -> int:
        """
        Метод для вызова метода для подсчета незаполненных подборок.

        :param file_path_collection: путь до документа Подборки.xlsx
        :return: количество незаполненных подборок
        """

        excel_manager = ExcelManager(file_path=file_path_collection)
        return excel_manager.count_empty_result()

    def _take_data_from_collection(
            self,
            file_path_collection: str,
            checking_unique: bool,
    ) -> dict:
        """
        Метод для загрузки данных по текущей подборке из таблицы Подборки.

        :param file_path_collection: путь до документа Подборки.xlsx
        :param checking_unique: параметр, который отвечает за запись или незапись хеша в таблицу
        :return: словарь с информацией о текущей подборке вида

            {'Возраст': '32',
             'Задача': 'Лучшее средство',
             'Запрос': 'ЗВ8',
             'Итог': None,
             'Лучший вариант': None,
             'Пол': 'женский',
             'Содержимое': 'Шампуни',
             'Специалист': 'Т',
             'Средства': ('AUSSIE Miracle Moist',
                          'ICE BY NATURA SIBERICA REFRESH MY SCALP',
                          'LADOR Keratin LPP',
                          'NATURA SIBERICA Oblepikha',
                          'PAYOT Shampoing doux biome-friendly',
                          'КУДРЯВЫЙ МЕТОД for curly hair'),
             'Тип': ('В1', 'В10'),
             'Хеш': -4256620288625128615}
        """

        excel_manager = ExcelManager(file_path=file_path_collection)
        return excel_manager.get_data_from_table_in_form_of_dict(
            ws_title="Подборки",
            checking_unique=checking_unique,
        )

    def _create_context_for_request_to_openai(
            self,
            prompt_for_convert: dict,
            json_scheme: dict,
            folder_name: str,
    ) -> str:
        """
        В этом методе осуществляется вызов ключевой функции по:
        1) созданию готового контекста, который передается в OpenAI,
        2) отправке самого запроса в OpenAI,
        3) сохранение результата

        :param prompt_for_convert: промпт для преобразования его в контекст
        :param json_scheme: схема с названиями папок
        :param folder_name: папка, в которую будет сохраняться ответ openai
        :return: путь до json файла с анализом средств
        """

        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')

        file_path_to_saving_json = appeal_to_openai_main(
            prompt=prompt_for_convert['prompt'],
            system_prompt=prompt_for_convert['system_prompt'],
            api_key=openai_api_key,
            json_scheme=json_scheme,
            folder_name=folder_name,
        )

        return file_path_to_saving_json

    def _reviewing_response_from_openai(
            self,
            file_path: str,
            json_file_path: str,
            dict_with_hash: dict,
    ) -> None:
        """
        Метод для разбора ответа от OpenAI.

        :param file_path: путь до документа Подборки.xlsx
        :param json_file_path: путь до json-файла с анализом средств
        :param dict_with_hash: словарь с текущей подборкой (для получения хеша)
        :return: None
        """

        # проверяю json-файл
        data = checking_file_with_response(json_file_path=json_file_path)

        # записываю в таблицу результат по анализу подборки
        excel_manager = ExcelManager(file_path=file_path)
        excel_manager.update_excel_with_json(
            data=data,
            dict_with_hash=dict_with_hash,
            file_path=file_path,
        )
        print('Данные по анализу подборки записаны в excel')

    # pylint: disable=R0913: too-many-arguments
    # pylint: disable=R0917: too-many-positional-arguments
    def _create_pdf_jpg(
            self,
            collection_data: dict,
            info_data: dict,
            selection_result: dict,
            path_to_output_folder_pdf_file: str,
            path_to_output_folder_jpg_file: str,
    ) -> None:
        """
        Готовит PDF и изображения

        :param collection_data: данные подборки
        :param info_data: данные с всеми средствами, врачами и т.д.
        :param selection_result: данные с результатом нейронки по подборке
        :param path_to_output_folder_pdf_file: путь к папке для сохранения PDF-файлов
        :param path_to_output_folder_jpg_file: путь к папке для сохранения JPG-файлов
        :return: None
        """

        create_pdf(
            collection_data=collection_data,
            info_data=info_data,
            selection_result=selection_result,
            path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
            path_to_output_folder_jpg_file=path_to_output_folder_jpg_file,
        )

        # # копируем файлы из папки telegram jpg в instagram jpg
        # copy_jpg_files(
        #     where_copy_from=paths_by_task[task_name]['jpg'],
        #     where_copy_to=self.paths_to_folders['instagram_jpg'],
        # )
        #
        # # копируем файлы из папки telegram jpg в pinterest jpg
        # copy_jpg_files(
        #     where_copy_from=paths_by_task[task_name]['jpg'],
        #     where_copy_to=self.paths_to_folders['pinterest_jpg'],
        # )

    def _forming_text_for_post(
            self,
            data: dict,
            info_for_picture: dict,
    ) -> None:
        """
        Метод для вызова функции по формированию текста для поста и его сохранение

        :param data: словарь с данными о пользователе и косметических средствах
        :param info_for_picture: словарь со средствами из подборки и итогом
        :return: None
        """

        # формируем текст для поста из нужных данных
        full_info = create_text_for_post(
            data=data,
            info_for_picture=info_for_picture
        )

        # Добавляем имя файла к пути
        output_file = Path(self.paths_to_folders["telegram_text"]) / "text_for_post.md"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(full_info)

    def create_collection(
            self,
            file_path_tools: str,
            file_path_collection: str,
            path_to_output_folder: str,
            checking_unique: bool,
    ) -> None:
        """
        Главный метод класса, в котором собрана вся логика программы

        :param file_path_tools: путь до таблицы со всей инфой о средствах, типах и прочем
        :param file_path_collection: путь до таблицы с подборками
        :param checking_unique: параметр, который отвечает за запись или незапись хеша в таблицу
        :param path_to_output_folder: путь до папки, в которую идет сохранение ответа от OpenAI,
        промпта, картинок и текста.

        :return: None
        """

        # забираю все данные из таблицы "Средства", "Тип", "Запрос" и т.д.
        data_tools = self._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )

        # захожу в "Подборки" и считаю сколько подборок не заполнено
        count_collection = self._get_count_collections(file_path_collection)

        for _ in range(count_collection):
            # формирую словарь с подборкой
            data_collection = self._take_data_from_collection(
                file_path_collection=file_path_collection,
                checking_unique=checking_unique,
            )

            # определяю json-схему
            json_scheme = get_json_scheme(
                data_collection=data_collection,
                product_categories=self.param_dif_products_categories,
            )

            # формирую пути для сохранения данных и создаю нужные папки
            self.paths_to_folders = DirsConstructor(
                base_output_folder_path=path_to_output_folder,
                data_collection=data_collection,
            ).get_output_folders()

            # cобираю промпт
            prompt = get_prompt(
                data_tools=data_tools,
                data_collection=data_collection,
            )

            print('Отправка запроса в OpenAI.')
            # pylint: disable=W0612 unused-variable
            file_path_to_saving_json = self._create_context_for_request_to_openai(
                prompt_for_convert=prompt,
                json_scheme=json_scheme,
                folder_name=self.paths_to_folders["00_source_02_answer_gpt"],
            )
            print('Смотрите ответ от OPENAI\n')


        # # file_path_to_saving_json будет содержать в себе
        # # 00_base/00_info_for_post/01_03_25/1_Шампуни/answer_gpt/Анализ_средств.json
        # print('Разбор ответа от OpenAI.')
        # self._reviewing_response_from_openai(
        #     file_path=file_path_collection,
        #     json_file_path=file_path_to_saving_json,
        #     dict_with_hash=data_collection,
        # )

        # print('Создание PDF и изображений со средствами для постов в соц.сети.')
        # self._create_pdf_jpg(
        #     collection_data=data_collection,
        #     info_data=data_tools,
        #     selection_result=checking_file_with_response(
        #         json_file_path=self.paths_to_folders["00_source_02_answer_gpt"]
        #     ),
        #     path_to_output_folder_pdf_file=self.paths_to_folders["00_source_03_pdf"],
        #     path_to_output_folder_jpg_file=self.paths_to_folders["00_source_04_jpg"],
        # )

        # # print('Готовлю текстовое оформление поста.')
        # # self._forming_text_for_post(data=data, info_for_picture=info_for_picture)
