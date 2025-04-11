"""
Главный модуль пост-конструктора.
"""
import re
from copy import deepcopy
from pathlib import Path

from pdf.main import create_textpost_pdf
from post_constructor.post_constructor import PostConstructor
from post_constructor.post_processing_data import build_description
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

    # получаем список из кортежей с названием средства и артикулом из текущей подборки
    products = get_products_list(data['Средства'])

    # список, в котором будут хештеги
    hashtag = []

    for product_title, product_article in products:
        product_title_lower = product_title.lower().strip()
        brand = data_tools['Средства'][product_title_lower][product_article]['Бренд']
        if brand:
            brand_no_space = re.sub(r'[^\wа-яА-ЯёЁ]+', '_', brand)
            hashtag.append(f"#{brand_no_space}")
        else:
            hashtag.append('#БРЕНД_ОТСУТСТВУЕТ')

    return ' '.join(set(hashtag))


# pylint: disable=R0913: too-many-arguments
# pylint: disable=R0917: too-many-positional-arguments
def create_post(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
        detailed: bool,
        file_name: str,
) -> None:
    """
    Универсальный генератор постов (короткая/подробная версия)
    """

    if collection_data['Параметры'].lower().strip() == 'учитывать':
        collection_data['Тип'] = build_description(
            code_string=collection_data['Тип'],
            section_data=data_tools['Тип'],
            detailed=detailed
        )

        collection_data['Запрос'] = build_description(
            code_string=collection_data['Запрос'],
            section_data=data_tools['Запрос'],
            detailed=detailed
        )

    # добавляем хештег
    collection_data['Хештег'] = create_hashtag(
        data=collection_data,
        data_tools=data_tools,
    )

    # создаём текст поста
    post_constructor = PostConstructor()
    info_for_post = post_constructor.create_text_for_post(
        data=collection_data,
        path_to_result_recommend=path_to_result_recommend,
        task=collection_data['Задача'],
    )

    # сохраняем
    save_file_in_process_work(
        data=info_for_post,
        path_to_folder=path_for_save,
        file_name=file_name,
        file_extension='.md',
    )


def create_post_detailed(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
) -> None:
    """
    Формирует длинную версию поста
    """
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
        detailed=True,
        file_name='text_for_post_detailed',
    )


def create_post_short(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
) -> None:
    """
    Формирует короткую версию поста
    """
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
        detailed=False,
        file_name='text_for_post_short',
    )


def forming_text_for_posts(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
) -> None:
    """
    Метод, в котором:
    1) расшифровываются данные из текущей подборки
    2) осуществляется формирование текста для поста и его сохранение

    :param data_tools: словарь со всеми данными по средствам
    :param collection_data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    :return: None
    """
    create_post_short(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
    )
    # здесь сохраняем пост в PDF
    create_textpost_pdf(
        path_to_text_post_file=str(Path(path_for_save) / 'text_for_post_short.md'),
        path_for_save_pdf_file=str(Path(path_for_save) / 'text_for_post_short.pdf'),
    )

    if collection_data['Параметры'].lower().strip() == 'учитывать':
        create_post_detailed(
            data_tools=data_tools,
            collection_data=deepcopy(collection_data),
            path_to_result_recommend=path_to_result_recommend,
            path_for_save=path_for_save,
        )
        # здесь сохраняем пост в PDF
        create_textpost_pdf(
            path_to_text_post_file=str(Path(path_for_save) / 'text_for_post_detailed.md'),
            path_for_save_pdf_file=str(Path(path_for_save) / 'text_for_post_detailed.pdf'),
        )
