import copy
from pprint import pprint

from prompt_constructor.prompt_constructor import PromptConstructor
from prompt_constructor.prompt_processing_data import PromptProcessingData


def get_prompt(
        data_tools: dict,
        data_collection: dict,
) -> dict:
    """
    Функция для вызова логики для расшифровки текущей подборки и создания промпта

    :param data_tools: словарь со всеми данными по средствам
    :param data_collection: словарь с текущей подборкой
    :return: промпт в виде словаря
    """

    # создание копии словаря с текущей подборкой,
    # т.к. иначе не добраться до кода задачи
    copy_data_collection = copy.deepcopy(data_collection)

    # расшифровка данных текущей подборки с помощью таблицы со всеми средствами
    prompt_proces_data = PromptProcessingData(
        data_tools=data_tools,
        data_collection=data_collection,
    )



    # получение словаря с полностью расшифрованными данными
    decrypted_collection = prompt_proces_data.main_decryp_data_from_current_collection(
        data_tools=data_tools,
        data_collection=data_collection,
    )
    pprint(decrypted_collection)

    prompt_constructor = PromptConstructor()

    # получение промпта для текущей подборки
    return prompt_constructor.main_constructor_prompt(
        data_decrypted=decrypted_collection,
        data_collection=copy_data_collection,
    )
