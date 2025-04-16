"""
Главный модуль пост-конструктора.
"""
import os
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


def create_products_info(
        data: dict,
        data_tools: dict,
        products_with_links: bool = False,
        products_with_articles: bool = False,
) -> str:
    """
    Получаем готовый абзац с названиями средств и их артикулами
    :param data: нерасшифрованный словарь с текущей подборкой
    :param products_with_links: названия средств с ссылками или нет
    :param products_with_articles: средства с артикулами
    :param data_tools: словарь со всеми данными по средствам

    :return: строку с информацией о псредствах и их артикулах
    """
    # получаем список из кортежей с названием средства и артикулом из текущей подборки
    products = get_products_list(data['Средства'])

    # список, в котором будут строки с информацией о продуктах
    products_info = []

    for title, article in products:
        display_title = title
        if products_with_links:
            product_data = data_tools['Средства'][title.lower().strip()][article]
            product_link = product_data.get('Ссылка в Золотом Яблоке')
            display_title = f'🔸 [{title}]({product_link})'

        line = display_title
        if products_with_articles:
            line += f': арт. {article}'
        products_info.append(f'{line}\n')

    return ''.join(products_info)


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
        products_with_links: bool = False,
) -> None:
    """
    Универсальный генератор постов (короткая/подробная версия)
    :param data_tools: словарь со всеми данными по средствам
    :param collection_data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    :param detailed: детализированная информация о пользователе или нет
    :param file_name: имя файла для сохранения
    :param products_with_links: вставлять в пост названия средств с ссылками или нет
    :return: None
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

    # добавляем информацию о средствах и  артикулах
    collection_data['Средства и артикулы'] = create_products_info(
        data=collection_data,
        data_tools=data_tools,
        products_with_links=products_with_links,

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
    :param data_tools: словарь со всеми данными по средствам
    :param collection_data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    """
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
        detailed=True,
        file_name='text_for_post_detailed',
        products_with_links=False,
    )


def create_text_post_for_telegram(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
) -> None:
    """
    Формирует текст для постинга в проверочныый канал
    1) Короткую версию
    1) Длинную версию

    :param data_tools: словарь со всеми данными по средствам
    :param collection_data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    """
    result_path_for_save = str(Path(path_for_save) / 'telegram_review/')
    os.makedirs(result_path_for_save, exist_ok=True)

    # Создаём короткую версию
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=result_path_for_save,
        detailed=False,
        file_name='text_for_review_post_short',
        products_with_links=True,
    )
    # Создаём длинную версию
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=result_path_for_save,
        detailed=True,
        file_name='text_for_review_post_detailed',
        products_with_links=True,
    )


def create_post_short(
        data_tools: dict,
        collection_data: dict,
        path_to_result_recommend: str,
        path_for_save: str,
) -> None:
    """
    Формирует короткую версию поста
    :param data_tools: словарь со всеми данными по средствам
    :param collection_data: нерасшифрованный словарь с текущей подборкой
    :param path_to_result_recommend: путь до json-файла, в котором находится
    ответ от GPT по подборке
    :param path_for_save: путь, по которому сохранять пост
    """
    create_post(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
        detailed=False,
        file_name='text_for_post_short',
        products_with_links=False,
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

    # создаём из поста в Markdown пост в виде JPG
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
        # создаём из поста в Markdown пост в виде JPG
        create_textpost_pdf(
            path_to_text_post_file=str(Path(path_for_save) / 'text_for_post_detailed.md'),
            path_for_save_pdf_file=str(Path(path_for_save) / 'text_for_post_detailed.pdf'),
        )

    create_text_post_for_telegram(
        data_tools=data_tools,
        collection_data=deepcopy(collection_data),
        path_to_result_recommend=path_to_result_recommend,
        path_for_save=path_for_save,
    )
