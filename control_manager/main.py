"""
В этом модуле - класс, управляющий логикой всего проекта
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from appeal_to_openai.main import main as appeal_to_openai_main
from appeal_to_openai.utils import checking_file_with_response
from control_manager.utils import create_dict_from_str
from dirs_structure_constructor.main import DirsConstructor
from excel_process_data.hash_utils import counting_hash, is_hash_unique
from excel_process_data.process_data import ExcelManager
from json_constructor.main import get_json_scheme
from post_constructor.main_post import forming_text_for_post
from prompt_constructor.main import get_prompt
from pdf.main import create_pdf
from utils.utils import save_file_in_process_work


# from utils.utils import copy_jpg_files


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

    def _get_collections(
            self,
            ws_title: str,
            file_path_collection: str,
            target_column_title: str,
            target_column_value: str | None,
    ) -> dict:
        """
        Метод для получения подборок, у которых определённое
        значение в определённом столбце.

        :param ws_title: имя листа с подборками
        :param file_path_collection: путь до документа Подборки.xlsx
        :param target_column_title: название целевого столбца
        :param target_column_value: значение, которое должно быть в целевом столбце
        :return: словарь с ключом - номер строки и вложенный словарь с данными
        подборки с заголовками столбцов
        """

        excel_manager = ExcelManager(file_path=file_path_collection)
        # Получаем словарь с подборками вида (номер строки: (кортеж с ячейками с данными))
        collections_data = excel_manager.get_rows_with_value_in_cell(
            ws_title=ws_title,
            target_column_title=target_column_title,
            target_column_value=target_column_value,
        )

        # Добавляем к данным названия столбцов для удобства
        for row_number, row_data in collections_data.items():
            data_with_row_title = excel_manager.load_info_about_collection(
                ws_title=ws_title,
                row=row_data,
            )
            collections_data[row_number] = data_with_row_title

        # Превращаем строку с средствами в словарь
        for row_number, row_data in collections_data.items():
            products = row_data.get("Средства")
            row_data["Средства"] = create_dict_from_str(_str=products)

        return collections_data

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

    # pylint: disable=R0913: too-many-arguments
    # pylint: disable=R0917: too-many-positional-arguments
    def update_collection_data_in_database(
            self,
            file_path_collection: str,
            ws_title: str,
            row: int,
            column_name: str,
            value: str | int | float,
    ) -> None:
        """
        Обновляет данные в подборке в указанном столбце

        :param file_path_collection: путь до документа Подборки.xlsx
        :param ws_title: Название листа
        :param row: Номер строки (начиная с 1)
        :param column_name: Название столбца (заголовок из первой строки)
        :param value: Значение для записи
        """

        excel_manager = ExcelManager(file_path=file_path_collection)

        excel_manager.write_value_to_cell(
            ws_title=ws_title,
            row=row,
            column_name=column_name,
            value=value,
        )

    # pylint: disable=R0917 too-many-arguments
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

    def recreate_pdf_and_posts(
            self,
            file_path_tools: str,
            file_path_collection: str,
            path_to_output_folder: str,
            progress_callback=None,
    ) -> None:
        """
        Метод для перегенерации PDF и постов

        :param file_path_tools: путь до таблицы со всей инфой о средствах, типах и прочем
        :param file_path_collection: путь до таблицы с подборками
        :param path_to_output_folder: путь до папки, в которую идет сохранение ответа от OpenAI,
        промпта, картинок и текста.
        :param progress_callback: колл-бек для отрисовки прогресс-бара

        :return: None
        """

        # Забираю все данные из таблицы "Средства", "Тип", "Запрос" и т.д.
        data_tools = self._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )
        # Захожу в "Подборки" и получаю все подборки для пересоздания постов и PDF
        collections = self._get_collections(
            ws_title='Подборки',
            file_path_collection=file_path_collection,
            target_column_title='Пересоздать PDF',
            target_column_value="да",
        )
        total = len(collections)
        for i, (row_number, collection_data) in enumerate(collections.items(), start=1):
            print(f'Готовим подборку из строки № {row_number}.')
            print('Считаем хеш и проверяем подборку на уникальность.')
            hash_collection = str(counting_hash(data=collection_data))
            result = is_hash_unique(
                ws_title='Подборки',
                file_path_collection=file_path_collection,
                hash_collection=hash_collection,
                row_number=row_number,
            )
            # если не уникальная подборка
            if result:
                print(f'При проверке хеша подборки в строке {row_number} нашли такой же хеш'
                      f' в строке {result} и выделили её красным')
                return None
            print('Подборка уникальна, продолжаем.')

            # Формирую пути для сохранения данных
            dirs_constructor = DirsConstructor(
                base_output_folder_path=path_to_output_folder,
                data_collection=collection_data,
            )
            self.paths_to_folders = (
                dirs_constructor
                .get_folder_paths(
                    category_folder=Path(collection_data['Путь'])
                )
            )
            print('Пересоздание PDF и изображений со средствами для постов в соц.сети.')
            self._create_pdf_jpg(
                collection_data=collection_data,
                info_data=data_tools,
                selection_result=checking_file_with_response(
                    json_file_path=self.paths_to_folders["00_source_02_answer_gpt"]
                ),
                path_to_output_folder_pdf_file=self.paths_to_folders["00_source_03_pdf"],
                path_to_output_folder_jpg_file=self.paths_to_folders["00_source_04_jpg"],
            )

            print('Пересоздание текстовой части постов.')
            forming_text_for_post(
                data_tools=data_tools,
                data=collection_data,
                path_to_result_recommend=self.paths_to_folders["00_source_02_answer_gpt"],
                path_for_save=self.paths_to_folders['00_source_05_text'],
            )

            # Обновляем "Хеш" подборки в таблице
            self.update_collection_data_in_database(
                file_path_collection=file_path_collection,
                ws_title='Подборки',
                row=row_number,
                column_name='Хеш',
                value=hash_collection,
            )

            # Вызов колбэка для обновления прогресс бара
            if progress_callback:
                progress_callback(i, total)

            print(f"Подборка из строки {row_number} готова 🌀\n")

        return None

    def create_collection(
            self,
            file_path_tools: str,
            file_path_collection: str,
            path_to_output_folder: str,
            progress_callback=None,
    ) -> None:
        """
        Метод для генерации новых подборок

        :param file_path_tools: путь до таблицы со всей инфой о средствах, типах и прочем
        :param file_path_collection: путь до таблицы с подборками
        :param path_to_output_folder: путь до папки, в которую идет сохранение ответа от OpenAI,
        промпта, картинок и текста.
        :param progress_callback: колл-бек для отрисовки прогресс-бара


        :return: None
        """

        # Забираю все данные из таблицы "Средства", "Тип", "Запрос" и т.д.
        data_tools = self._take_data_from_table_tool(
            file_path_tools_table=file_path_tools,
        )
        # Захожу в "Подборки" и получаю новые подборки (которые ещё без пути сохранения)
        collections = self._get_collections(
            ws_title='Подборки',
            file_path_collection=file_path_collection,
            target_column_title='Путь',
            target_column_value="",
        )
        total = len(collections)
        for i, (row_number, collection_data) in enumerate(collections.items(), start=1):
            print(f'Готовим подборку из строки № {row_number}.')
            print('Считаем хеш и проверяем подборку на уникальность.')
            hash_collection = str(counting_hash(data=collection_data))
            result = is_hash_unique(
                ws_title='Подборки',
                file_path_collection=file_path_collection,
                hash_collection=hash_collection,
                row_number=row_number,
            )
            # если не уникальная подборка
            if result:
                print(f'При проверке хеша подборки в строке {row_number} нашли такой же хеш'
                      f' в строке {result} и выделили её красным')
                return None
            print('Подборка уникальна, продолжаем.')

            # Формирую пути для сохранения данных и создаю нужные папки
            self.paths_to_folders = DirsConstructor(
                base_output_folder_path=path_to_output_folder,
                data_collection=collection_data,
            ).get_output_folders(
                prefix=collection_data['Группа'],
            )

            # Определяю json-схему
            json_scheme = get_json_scheme(
                data_collection=collection_data,
                product_categories=self.param_dif_products_categories,
            )

            # Сохраняем json-схему в папку
            save_file_in_process_work(
                what_save=json_scheme,
                path_to_folder=self.paths_to_folders['00_source_00_json_scheme'],
                file_name='json_scheme',
                file_extension='.json',
            )

            # Собираю промпт
            prompt = get_prompt(
                data_tools=data_tools,
                data_collection=collection_data,
            )

            # Сохраняем prompt в папку
            save_file_in_process_work(
                what_save=prompt,
                path_to_folder=self.paths_to_folders['00_source_01_prompt'],
                file_name='prompt',
                file_extension='.json',
            )

            print('Отправка запроса в OpenAI.')
            self._create_context_for_request_to_openai(
                prompt_for_convert=prompt,
                json_scheme=json_scheme,
                folder_name=self.paths_to_folders["00_source_02_answer_gpt"],
            )

            print('Создание PDF и изображений со средствами для постов в соц.сети.')
            self._create_pdf_jpg(
                collection_data=collection_data,
                info_data=data_tools,
                selection_result=checking_file_with_response(
                    json_file_path=self.paths_to_folders["00_source_02_answer_gpt"]
                ),
                path_to_output_folder_pdf_file=self.paths_to_folders["00_source_03_pdf"],
                path_to_output_folder_jpg_file=self.paths_to_folders["00_source_04_jpg"],
            )

            print('Готовлю текстовое оформление поста.')
            forming_text_for_post(
                data_tools=data_tools,
                data=collection_data,
                path_to_result_recommend=self.paths_to_folders["00_source_02_answer_gpt"],
                path_for_save=self.paths_to_folders['00_source_05_text'],
            )

            # Обновляем "Путь" подборки в таблице
            self.update_collection_data_in_database(
                file_path_collection=file_path_collection,
                ws_title='Подборки',
                row=row_number,
                column_name='Путь',
                value=self.paths_to_folders['folder_path'],
            )

            # Обновляем "Хеш" подборки в таблице
            self.update_collection_data_in_database(
                file_path_collection=file_path_collection,
                ws_title='Подборки',
                row=row_number,
                column_name='Хеш',
                value=hash_collection,
            )

            # Вызов колбэка для обновления прогресс бара
            if progress_callback:
                progress_callback(i, total)

            print(f"Подборка из строки {row_number} готова 🌀\n")

        return None
