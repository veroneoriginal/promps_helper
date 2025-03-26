"""
Главный модуль пост-конструктора.
"""

from prompt_constructor.prompt_processing_data import PromptProcessingData
from post_constructor.post_constructor import PostConstructor
from utils.utils import save_file_in_process_work

def forming_text_for_post(
        data_tools: dict,
        data: dict,
        path_to_result_recommend: str,
        path_for_save:str,
) -> None:
    """
    Метод, в котором:
    1) расшифровываются данные из текущей подборки
    2) осуществляется формирование текста для поста и его сохранение

    :param data_tools: словарь со всеми данными по средствам
    :param data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    :return: None
    """

    # т.к. из исходного словаря мне нужно расшифровать только запрос и тип

    # расшифровка данных текущей подборки с помощью таблицы со всеми средствами
    prompt_proces_data = PromptProcessingData(
        data_tools=data_tools,
        data_collection=data,
    )

    # расшифровываем ключ тип
    data['Тип'] = prompt_proces_data.decrypting_data_from_cell(
        data=data_tools,
        data_collection=data,
        key_for_decrypted="Тип",
    )

    # расшифровываем ключ запрос
    data['Запрос'] = prompt_proces_data.decrypting_data_from_cell(
        data=data_tools,
        data_collection=data,
        key_for_decrypted="Запрос",
    )
    # на этом этапе в исходном словаре обновилось 2 ключа

    # формируем текст для поста из нужных данных
    post_constructor = PostConstructor()

    info_for_post = post_constructor.create_text_for_post(
        data=data,
        path_to_result_recommend=path_to_result_recommend,
        task=data['Задача'],
    )

    # сохраняем результат
    save_file_in_process_work(
        what_save=info_for_post,
        path_to_folder=path_for_save,
        file_name='text_for_post',
        file_extension='.md',
    )
