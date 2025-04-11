import math
import os
from copy import deepcopy

from dotenv import load_dotenv

from appeal_to_openai.main import send_request_to_openai
from json_constructor.main import get_json_scheme
from prompt_constructor.main import get_prompt
from task_processing.utils import merge_json_files, get_list_composition_elements
from utils.utils import save_file_in_process_work


class TaskProcessing:
    """
    Класс для выполнения задач по разборам средств
    """

    def __init__(
            self,
            data_tools: dict,
            collection_data: dict,
            paths_to_save_folders: dict,
    ):
        """
        :param data_tools: база данных средств и всего остального
        :param collection_data: данные подборки
        :param paths_to_save_folders: пути до папок для сохранения
        """
        self.data_tools = data_tools
        self.collection_data = collection_data
        self.paths_to_save_folders = paths_to_save_folders

        self.method_for_task_code = {
            'Подробный анализ состава': self.detailed_analysis_composition,
            'Лучшее средство': self.task_with_one_step,
            'Лучшее средство без канцерогенов':
                self.task_with_one_step,
            'Разбор состава одного средства': self.task_with_one_step,
            'Лучшая пара': self.task_with_one_step,
            'Лучшее сочетание': self.task_with_one_step,
            'Лучшая компоновка': 'метод создает json-схему для текущей подборки по коду задачи',
            'Аналог': self.task_with_one_step,
            'Наиболее похож': 'метод создает json-схему для текущей подборки по коду задачи',
            'Наименее похож': 'метод создает json-схему для текущей подборки по коду задачи',
        }

    def request_to_openai(
            self,
            prompt_for_convert: dict,
            json_scheme: dict,
    ) -> str:
        """
        В этом методе осуществляется вызов ключевой функции по:
        1) созданию готового контекста, который передается в OpenAI,
        2) отправке самого запроса в OpenAI,
        3) сохранение результата

        :param prompt_for_convert: промпт для преобразования его в контекст
        :param json_scheme: схема с названиями папок
        :return: путь до json файла с анализом средств
        """

        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        openai_model = os.getenv('OPENAI_MODEL')

        return send_request_to_openai(
            prompt=prompt_for_convert['prompt'],
            system_prompt=prompt_for_convert['system_prompt'],
            api_key=openai_api_key,
            json_scheme=json_scheme,
            model=openai_model,
        )

    def run_task_processing(self):
        """
        Формируем "шаги" задачи и запускаем процесс выполнения задачи.
        """

        task = self.collection_data['Задача']
        self.method_for_task_code[task]()

    def run_task_step(
            self,
            step_collection_data: dict,
            task_step_number: int,
    ) -> None:
        """
        Выполняем один шаг задачи.
        В один шаг входит:
        1) Подготовка данных
        2) Создание json-схемы и её сохранение
        3) Создание промпта и его сохранение
        4) Отправка запроса в OpenAI и сохранение ответа

        :param step_collection_data: подготовленные данные подборки для шага задачи
        :param task_step_number: номер шага задачи

        """

        # Определяю json-схему
        json_scheme = get_json_scheme(
            data_tools=self.data_tools,
            data_collection=step_collection_data,
        )

        # Сохраняем json-схему в папку
        save_file_in_process_work(
            data=json_scheme,
            path_to_folder=self.paths_to_save_folders['00_json_scheme'],
            file_name=f'{task_step_number}_step_json_scheme',
            file_extension='.json',
        )
        # Собираю промпт
        prompt = get_prompt(
            data_tools=self.data_tools,
            data_collection=step_collection_data,
        )

        # Сохраняем prompt в папку
        save_file_in_process_work(
            data=prompt,
            path_to_folder=self.paths_to_save_folders['01_prompt'],
            file_name=f'{task_step_number}_step_prompt',
            file_extension='.json',
        )

        print('Отправка запроса в OpenAI.')
        answer_openai = self.request_to_openai(
            prompt_for_convert=prompt,
            json_scheme=json_scheme,
        )
        # Сохраняем ответ OpenAI в папку
        save_file_in_process_work(
            data=answer_openai,
            path_to_folder=self.paths_to_save_folders["02_answer_gpt"],
            file_name=f'{task_step_number}_step_answer_gpt',
            file_extension='.json',
        )

    def run_all_task_steps(
            self,
            all_task_steps: list,
    ) -> None:
        """
        Выполнить все шаги задачи
        :param all_task_steps: все шаги задачи в виде списка
        """

        for step_number, step_data in all_task_steps:
            self.run_task_step(
                step_collection_data=step_data,
                task_step_number=step_number
            )
        # объединяем ответы OpenAI в один json-файл
        merge_json_files(
            folder_path=self.paths_to_save_folders["02_answer_gpt"],
            output_filename='Анализ_средств.json',
        )

    def task_with_one_step(self):
        """
        Выполнение задачи с одним шагом.
        """

        step_data = self.collection_data
        task_steps = [
            (0, step_data)
        ]

        self.run_all_task_steps(all_task_steps=task_steps)

    def detailed_analysis_composition(self):
        """
        Выполнение задачи 'Подробный анализ состава'
        """

        # Максимальное количество элементов в составе средства для одного шага в задаче
        MAX_ELEMENTS_IN_STEP = 10

        # Получаем список вида ['1_Aqua (Water)', '2_Behentrimonium chloride', ...]
        numbered_composition_elements_list = get_list_composition_elements(
            data_tools=self.data_tools,
            collection_data=self.collection_data,
        )
        # Вычисляем количество шагов в задаче
        task_steps_count = math.ceil(len(numbered_composition_elements_list) / MAX_ELEMENTS_IN_STEP)
        # Формируем шаги задачи
        task_steps = []
        for step_number in range(task_steps_count):
            # Вычисляем индексы для срезов для элементов
            start_index = step_number * MAX_ELEMENTS_IN_STEP
            end_index = step_number * MAX_ELEMENTS_IN_STEP + MAX_ELEMENTS_IN_STEP
            # Добавляем в подборку нужную информацию:
            step_collection_data = deepcopy(self.collection_data)
            step_collection_data['Элементы состава для шага задачи'] = (
                numbered_composition_elements_list[start_index:end_index]
            )
            # Добавляем шаг
            task_steps.append(
                (step_number, step_collection_data)
            )
        self.run_all_task_steps(all_task_steps=task_steps)
