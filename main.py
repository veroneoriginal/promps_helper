"""
В этом модуле - класс, управляющий логикой всего проекта
"""

import os
from datetime import datetime
from pathlib import Path
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
from source.structure_folders.structure_folders import scheme_for_folders_name



class ControlManager:
    """
    Класс, управляющий логикой весго проекта
    """

    def __init__(self, scheme_for_folders):
        self.paths_to_folders = {}
        self.scheme_for_folders = scheme_for_folders

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
            folder_name: str,
    ) -> str:
        """
        В этой функции осуществляется вызов ключевой функции по:
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
            prompt=prompt_for_convert,
            system_prompt=SYSTEM_PROMPT,
            api_key=openai_api_key,
            json_scheme=json_scheme,
            folder_name=folder_name,
        )

        return file_path_to_saving_json

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

        :param category_folder:  Путь к папке подборки
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
        Создает папки для сохранения файлов и возвращает их пути.

        :param category: название категории для подпапки.
        :param path_to_output_folder: путь до основной папки, в которую идет сохранение.

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

    def _create_pdf_jpg_for_post(
            self,
            info_for_picture: dict,
    ) -> None:
        """
        Метод для создания pdf-листов в телеграм (для постов со средствами)

        :param info_for_picture: словарь со всеми данными по средствам
        :return: None
        """
        # из огромного словаря со всеми данными, берем инфу для картинки в пост
        list_with_info = forming_indo_for_pdf(data=info_for_picture)

        create_pdf = PDFCreator()
        create_pdf.gen_pages_for_six_product(
            list_with_info=list_with_info,
            # Формируем путь для сохранения
            output_folder_pdf=self.paths_to_folders['telegram_pdf'],
            output_folder_jpg=self.paths_to_folders["telegram_jpg"],
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
            category: str,
            path_to_output_folder: str,
            product_count: int = 6 | 4,
    ) -> None:
        """
        Главный метод класса, в котором собрана вся логика программы

        :param category: категория, по которой осуществляется по подборка
        :param product_count: количество средств, которые анализируюся
        :param path_to_output_folder: путь до папки, в которую идет сохранение.
        :return: None
        """

        # Исходя из категории, формируем путь до документа .xlsx
        file_path = f'00_base/{category}.xlsx'

        print('Формирую пути сохранения данных.')
        self._get_output_folders(
            path_to_output_folder=path_to_output_folder,
            category=category,
        )

        print('Определяю json-схему.')
        json_scheme = self._determine_scheme_for_response_format(product_count=product_count)

        print('Забираю данные из таблицы.')
        data = self._take_data_from_the_table(file_path=file_path)

        print('Собираю промпт.')
        prompt = self._bring_prompt(dict_with_info=data)

        print('Отправляю запрос в OpenAI.')
        file_path_to_saving_json = self._create_context_for_request_to_openai(
            prompt_for_convert=prompt,
            json_scheme=json_scheme,
            folder_name=self.paths_to_folders["prompt"],
        )

        print('Разбираю ответ от OpenAI.')
        self._reviewing_response_from_openai(file_path=file_path,
                                             json_file_path=file_path_to_saving_json)

        print('Формирую данные для картинок.')
        info_for_picture = self._generating_data_for_images(file_path=file_path)

        print('Готовлю текстовое оформление поста.')
        self._forming_text_for_post(data=data, info_for_picture=info_for_picture)

        print('Создаю изображения со средствами для Telegram-поста.')
        self._create_pdf_jpg_for_post(
            info_for_picture=info_for_picture
        )


if __name__ == '__main__':
    instance = ControlManager(scheme_for_folders=scheme_for_folders_name)
    instance.create_collection(
        category="Шампуни",
        product_count=6,
        path_to_output_folder='00_base/00_info_for_post/',
    )
