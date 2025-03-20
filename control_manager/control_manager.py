# pylint: disable=W0612 unused-variable
"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
import json
from datetime import datetime
from pathlib import Path

from pprint import pprint

from dotenv import load_dotenv
from appeal_to_openai.main import main as appeal_to_openai_main
from appeal_to_openai.utils import checking_file_with_response
from excel_process_data.process_data import ExcelManager
from pdf.main_pdf import PDFCreator
from pdf.utils import main_forming_info_for_pdf
from post_constructor.post_constructor import create_text_for_post
from json_constructor.main import get_json_scheme
from prompt_constructor.main import get_prompt

from utils.utils import (
    copy_jpg_files,
    transforming_dict_from_json_file,
    add_keys_from_another_dict_to_one_dict,
)


class ControlManager:
    """
    Класс, управляющий логикой всего проекта
    """

    def __init__(self, scheme_for_folders, param_dif_products_categories):
        self.paths_to_folders = {}
        self.scheme_for_folders = scheme_for_folders
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

    def _create_timestamped_folder(
            self,
            path_to_output_folder: str,
    ) -> Path:
        """
        Метод для определения базовой папки с текущей датой для сохранения файлов

        :param path_to_output_folder: путь до основной папки, в которую идет сохранение.
        :return: объект Path с путем к базовой папке
        """

        # Получаем текущую дату в формате ДД_ММ_ГГ
        timestamp = datetime.now().strftime("%d_%m_%y")

        # Определяем базовую папку
        base_output_folder = Path(path_to_output_folder) / timestamp
        base_output_folder.mkdir(parents=True, exist_ok=True)

        return base_output_folder

    def _get_existing_folders(
            self,
            base_output_folder: Path,
    ) -> list:
        """
        Метод получает список существующих папок в указанной директории с текущей датой.

        :param base_output_folder: Путь к базовой директории с текущей датой
        :return: список объектов Path, представляющих папки
        """
        existing_folders = []
        for folder in base_output_folder.iterdir():
            if folder.is_dir():
                existing_folders.append(folder)

        return existing_folders

    def _get_new_folder_number(
            self,
            existing_folders: list,
    ) -> int:
        """
        Определяет новый номер для папки на основе существующих папок.

        :param existing_folders: Список объектов Path, представляющих папки
        :return: Новый номер папки
        """

        # если список пустой
        if not existing_folders:
            return 1

        last_number = 0

        for folder in existing_folders:
            name_parts = folder.name.split('_')
            if name_parts[0].isdigit():
                number = int(name_parts[0])
                last_number = max(last_number, number)

        return last_number + 1

    def _create_category_folder(
            self,
            base_output_folder: Path,
            new_folder_number: int,
            category: str,
    ) -> Path:
        """
        Создаёт папку категории с именем, состоящим из номера и названия категории,
        например, 1_Шампуни

        :param base_output_folder: Базовая выходная папка, где будет создана новая папка
        :param new_folder_number: Номер новой папки
        :param category: Название категории
        :return: Путь к созданной папке категории
        """
        category_folder_name = f"{new_folder_number}_{category}"
        category_folder = base_output_folder / category_folder_name
        category_folder.mkdir(exist_ok=True)
        return category_folder

    def _get_folder_paths(
            self,
            category_folder: Path,
    ) -> None:
        """
        Создает словарь путей ко всем созданным папкам соцсетей и их подпапкам.

        :param category_folder: Путь к папке подборки
        :return: None (изменяет self.paths_to_folders)
        """

        for service, folders in self.scheme_for_folders.items():
            service_path = category_folder / service

            # Если список подпапок пустой или отсутствует, добавляем только базовый путь сервиса
            if not folders or not isinstance(folders, list):
                self.paths_to_folders[service] = str(service_path)

            for folder in folders:
                key = f"{service}_{folder}"
                # Получаем полный путь и преобразуем в строку
                full_path = str(service_path / folder)
                # записываем в словарь
                self.paths_to_folders[key] = full_path

    def _create_subfolders(self) -> None:
        """
        Проходим по словарю self.paths_to_folders и создаем папки.

        :return: None
        """

        for folder_path in self.paths_to_folders.values():
            # Преобразуем путь в объект Path
            path = Path(folder_path)

            # Создаём папку (parents=True — создаёт все родительские папки,
            # exist_ok=True — не выдаёт ошибку, если папка уже есть)
            path.mkdir(parents=True, exist_ok=True)

    def _get_output_folders(
            self,
            path_to_output_folder: str,
            category: str,
    ) -> None:
        """
        Метод для создания папки для сохранения файлов.

        :param path_to_output_folder: путь до основной папки, в которую идет сохранение.
        :param category: название категории для подпапки (для текущей подборки).
        :return: None
        """

        # Определяем базовую папку
        base_output_folder = self._create_timestamped_folder(
            path_to_output_folder=path_to_output_folder
        )

        # Получаем список существующих папок в базовой директории
        existing_folders = self._get_existing_folders(
            base_output_folder=base_output_folder,
        )

        # Определяем новый номер папки
        new_folder_number = self._get_new_folder_number(
            existing_folders=existing_folders,
        )

        # Формируем имя новой папки - номер и с чем подборка
        category_folder = self._create_category_folder(
            base_output_folder=base_output_folder,
            new_folder_number=new_folder_number,
            category=category,
        )

        # Наполняем self.paths_to_folders путями до каждой конкретной папки
        self._get_folder_paths(category_folder=category_folder)

        # Создаем папки для соц.сетей и их внутренние папки с категориями
        self._create_subfolders()

    def _forming_data_for_images(
            self,
            json_file_path: str,
            data_tools: dict,
    ) -> dict:
        """
        Метод для формирования общего словаря со средствами, их плюсами и минусами и т.д.

        :param json_file_path: путь до json-файла с анализом средств
        :param data_tools: словарь с информацией о средствах, типах и прочем
        :return: словарь со средствами, их плюсами и минусами, и соотношенияем объема и цены
        """

        # обращаемся к json файлу
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # удаляю ненужные ключи из словаря
        if 'best_product' in data.keys() and 'result' in data.keys():
            del data['best_product']
            del data['result']

        # трансформирую словарь из json-a в словарь, где ключи - названия средств
        transformed_dict = transforming_dict_from_json_file(data=data)

        # Список ключей, которые нужно добавить
        required_keys = [
            "Количество меры (число)",
            "Юниты меры (мл/шт)",
            "Стоимость руб",
            "Ссылка на изображение в базе",
            "Тип продукта",
        ]

        # дополняю transformed_dict ключами из data_tools
        return add_keys_from_another_dict_to_one_dict(
            base_dict=data_tools,
            transform_dict=transformed_dict,
            list_keys=required_keys,
        )

    def _create_pdf_jpg_for_post(
            self,
            data: dict,
            data_task: dict,
    ) -> None:
        """
        Метод для создания pdf-листов и jpg-файлов (для постов со средствами)

        :param data: словарь со средствами, их плюсами, минусами и прочим
        :param data_task: словарь с кодом задачи, количеством средств, категорией продукта
        :return: None
        """

        task_name = data_task["Задача"]

        create_pdf = PDFCreator()

        generation_pictures = {

            'Лучшее средство': create_pdf.gen_pages_for_six_product,
            'Лучшее средство без канцерогенов': create_pdf.gen_pages_for_six_product,
            'Разбор состава одного средства': create_pdf.gen_pages_for_one_product,

        }

        # Получаем пути для сохранения файлов
        paths_by_task = {
            'Лучшее средство': {
                'pdf': self.paths_to_folders['telegram_pdf'],
                'jpg': self.paths_to_folders['telegram_jpg'],
            },
            'Лучшее средство без канцерогенов': {
                'pdf': self.paths_to_folders['telegram_pdf'],
                'jpg': self.paths_to_folders['telegram_jpg'],
            },
            'Разбор состава одного средства': {
                'pdf': self.paths_to_folders['telegram_pdf'],
                'jpg': self.paths_to_folders['telegram_jpg'],
            },
        }

        # формируем инфу для картинки в пост
        list_with_info = main_forming_info_for_pdf(
            data=data,
            data_task=data_task,
            product_categories=self.param_dif_products_categories,
        )
        print(f'{list_with_info=}')
        # Вызываем нужную функцию генерации
        generation_func = generation_pictures.get(task_name)

        generation_func(
            info=list_with_info,
            # Формируем путь для сохранения
            output_folder_pdf=paths_by_task[task_name]['pdf'],
            output_folder_jpg=paths_by_task[task_name]['jpg'],
        )

        # копируем файлы из папки telegram jpg в instagram jpg
        copy_jpg_files(
            where_copy_from=paths_by_task[task_name]['jpg'],
            where_copy_to=self.paths_to_folders['instagram_jpg'],
        )

        # копируем файлы из папки telegram jpg в pinterest jpg
        copy_jpg_files(
            where_copy_from=paths_by_task[task_name]['jpg'],
            where_copy_to=self.paths_to_folders['pinterest_jpg'],
        )

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

        # for _ in range(count_collection):
        # формирую словарь с первой подборкой
        data_collection = self._take_data_from_collection(
            file_path_collection=file_path_collection,
            checking_unique=checking_unique,
        )
        print('Перед json схемой')
        pprint(data_collection)
        print()


        # определяю json-схему
        json_scheme = get_json_scheme(
            data_collection=data_collection,
            product_categories=self.param_dif_products_categories,
        )
        # pprint(json_scheme)

        # формирую путь для сохранения данных
        self._get_output_folders(
            path_to_output_folder=path_to_output_folder,
            category=data_collection['Категория'],
        )

        # cобираю промпт
        prompt = get_prompt(
            data_tools=data_tools,
            data_collection=data_collection,
        )

        print('cобираю промпт')
        pprint(prompt)

        # print('Отправка запроса в OpenAI.')
        # # self.paths_to_folders["answer_gpt"] будет содержать в себе
        # # 00_base/00_info_for_post/01_03_25/1_Шампуни/answer_gpt
        # file_path_to_saving_json = self._create_context_for_request_to_openai(
        #     prompt_for_convert=prompt,
        #     json_scheme=json_scheme,
        #     folder_name=self.paths_to_folders["answer_gpt"],
        # )
        #
        # # file_path_to_saving_json будет содержать в себе
        # # 00_base/00_info_for_post/01_03_25/1_Шампуни/answer_gpt/Анализ_средств.json
        # print('Разбор ответа от OpenAI.')
        # self._reviewing_response_from_openai(
        #     file_path=file_path_collection,
        #     json_file_path=file_path_to_saving_json,
        #     dict_with_hash=data_collection,
        # )
        #
        #
        # print('Формирование данных для картинок')
        # data_for_images = self._forming_data_for_images(
        #     json_file_path=file_path_to_saving_json,
        #     data_tools=data_tools['Средства'],
        # )
        #
        # pprint(f'{data_for_images=}')
        # print('Создание картинок со средствами для постов в соц.сети.')
        # self._create_pdf_jpg_for_post(
        #     data=data_for_images,
        #     data_task=data_for_dif_tasks,
        # )
        #
        # print()

        # # print('Готовлю текстовое оформление поста.')
        # # self._forming_text_for_post(data=data, info_for_picture=info_for_picture)
