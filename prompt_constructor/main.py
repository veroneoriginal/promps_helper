import copy

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
        data_collection=copy_data_collection,
    )
    # получение словаря с полностью расшифрованными данными
    decrypted_collection = prompt_proces_data.main_decryp_data_from_current_collection(
        data_tools=data_tools,
        data_collection=copy_data_collection,
    )

    prompt_constructor = PromptConstructor()

    # получение промпта для текущей подборки
    result = prompt_constructor.main_constructor_prompt(
        data_decrypted=decrypted_collection,
        task=data_collection['Задача'],
    )
    # print("Функция get_prompt")
    # pprint(f"{result=}")
    # print()
    # result выглядит таким образом
    # {'prompt': 'Информация о средстве и его составе: Средство_1 - ONLY BIO EXTRA '
    #            'VIRGIN Almond de provence. Артикул: 19000286585. Состав: 1_Aqua, '
    #            '2_Sodium Lauroyl Sarcosinate, 3_Cocamidopropyl Betaine, 4_Lauryl '
    #            'Glucoside, 5_Caprylyl/decyl Glucoside, 6_Glycerin, 7_PEG-120 '
    #            'Methyl Glucose Dioleate, 8_Benzyl Alcohol, 9_Tropaeolum Majus '
    #            'Flower/leaf/stem Extract (oxygeskin®), 10_Olea Europaea Fruit Oil. '
    #            'Тип продукта: шампунь. .\n'
    #            'Учти всю вышепредставленную информацию и проведи анализ каждого '
    #            'элемента состава. \n'
    #            'Сохраняй нумерацию элементов.\n'
    #            '    Ответ ты должен дать в следующем виде: Тебе дано средство и '
    #            'часть элементов его состава. Тебе надо разобрать каждый элемент '
    #            'состава средства. Внимательно изучаешь и выдаёшь результат в '
    #            'соответствии с json схемой. Ответы должны быть понятны человеку '
    #            'без медицинского образования, старайся отвечать понятно, без '
    #            'сложных формулировок. Отвечай всегда на русском языке.',
    #  'system_prompt': 'Трихолог'}
    return result
