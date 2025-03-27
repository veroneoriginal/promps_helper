"""
Главный модуль пост-конструктора.
"""

from prompt_constructor.prompt_processing_data import PromptProcessingData
from post_constructor.post_constructor import PostConstructor
from utils.utils import save_file_in_process_work


def get_products_list(
        products_dict: dict,
) -> list:
    """
    Функция для получения средств из текущей подборки

    :param products_dict: словарь со средствами из текущей подборки
    :return: список с названиями средств из текущей подборки
    """
    products_list = []

    # Получаем все значения первого уровня
    for value in products_dict.values():
        # Если значение само является словарем (для кода задачи с наборами)
        if isinstance(value, dict):
            products_list.extend(value.values())
        # Если значение - строка (для всех остальных)
        else:
            products_list.append(value)

    return products_list


def create_hashtag(
        data_tools: dict,
        data: dict,
) -> str:
    """
    Функция, с помощью которого получаем названия брендов и превращаем их в хештеги

    :param data_tools: словарь со всеми данными по средствам
    :param data: нерасшифрованный словарь с текущей подборкой

    :return: возвращает строку с хештегами брендов по теукущей подборке
    """

    # получаем список средств из текущей подборки
    products = get_products_list(data['Средства'])

    # список, в котором будут хештеги
    hashtag = []

    for product in products:
        brand = data_tools['Средства'][product]['Бренд']
        if brand:
            brand_no_space = ''.join(brand.split())
            hashtag.append(f"#{brand_no_space}")
        else:
            brand_no_space = 'БРЕНД_ОТСУТСТВУЕТ'
            hashtag.append(f"#{brand_no_space}")

    return ' '.join(hashtag)


def forming_text_for_post(
        data_tools: dict,
        data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
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

    # добавляем хештег
    data['Хештег'] = create_hashtag(
        data=data,
        data_tools=data_tools,
    )

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
