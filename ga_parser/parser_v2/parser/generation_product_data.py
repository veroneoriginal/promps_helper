# pylint: disable=R0914: wildcard-import

"""
Логика для обработки данных из словаря с карточной средства
"""
import json
import re
from pathlib import Path

from bs4 import (
    BeautifulSoup,
    Tag,
    NavigableString,
)

from ga_parser.utils.utils import (
    clean_product_name,
    clean_text_2,
    leave_numbers,
)


def get_product_data_dict(
        html: str,
        image_dir_path: str,
) -> dict:
    """
    Формирования финального словаря со всеми данными по средству

    :param html: html-контент в виде строки
    :param image_dir_path: путь до изображения
    :return: dict
    """

    soup = BeautifulSoup(html, 'html.parser')

    detailed_product_type = get_detailed_product_type(soup=soup)
    (
        product_id,
        product_name,
        product_description,
    ) = get_item_title_description(soup=soup)
    characteristics = get_characteristics(soup=soup)
    application_instruction = get_application_instruction(soup=soup)
    compound = get_compound(soup=soup)

    (
        brand_name,
        brand_country,
        brand_description,
    ) = get_brand(soup=soup)

    price = get_price_in_stock(soup=soup)
    (
        measure,
        measure_units,
        measure_quantity
    ) = get_measure(characteristics=characteristics)
    img_link = get_img_link(soup=soup)
    img_link_in_base = get_img_link_in_base(
        product_title=product_name,
        product_id=product_id,
        image_dir_path=image_dir_path
    )
    additional_info = get_additional_info(soup=soup)

    return {
        'Название': product_name,
        'Тип продукта': characteristics.get('тип продукта', None),
        'Тип продукта подробно': detailed_product_type,
        'Для кого': characteristics.get('для кого', None),
        'Назначение': characteristics.get('назначение', None),
        'Тип волос': characteristics.get('тип волос', None),
        'Тип кожи': characteristics.get('тип кожи', None),
        'Область применения': characteristics.get('область применения', None),
        'Артикул в Золотом Яблоке': product_id,
        'Описание': product_description,
        'Характеристики': json.dumps(characteristics, ensure_ascii=False),
        'Применение': application_instruction,
        'Состав': compound,
        'Бренд': brand_name,
        'Страна бренда': brand_country,
        'Описание бренда': brand_description,
        'Стоимость руб': price,
        'Мера (объём/количество)': measure,
        'Количество меры (число)': measure_quantity,
        'Юниты меры (мл/шт)': measure_units,
        'Ссылка на изображение': img_link,
        'Ссылка на изображение в базе': img_link_in_base,
        'Дополнительная информация': additional_info,
        'Заполнено': 'да',
    }


def get_detailed_product_type(
        soup: Tag | NavigableString,
) -> str:
    """
    Для получения: Верхнее описание ,

    :param soup: суп из HTML-контента
    :return: str
    """

    h1 = soup.find("h1")
    if h1:
        parent = h1.parent
        # Ищем первый <div> с текстом
        target_div = parent.find("div")
        if target_div:
            upper_description = clean_text_2(target_div.get_text(strip=True))
        else:
            upper_description = None
    else:
        upper_description = None

    return upper_description


def get_characteristics(
        soup: Tag | NavigableString,
) -> dict:
    """
    Для получения: Тип продукта, Для кого, Назначение, Тип волос,
    Тип кожи, Область применения, Текстура, Финиш, Объём

    :param soup: суп из HTML-контента
    :return: tuple
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(name='div', attrs={'value': 'Description_0'})
    # Ищем весь блок Описание
    product_description_block = all_description_block.find(name='div', attrs={'text': 'Описание'})
    characteristics_block = product_description_block.find(name='dl')

    characteristics = {}
    for div in characteristics_block.find_all('div')[1:]:
        dt_list = div.find_all('dt')
        key = clean_text_2(dt_list[0].get_text())
        value = clean_text_2(dt_list[1].get_text())
        characteristics[key] = value

    return characteristics


def get_item_title_description(
        soup: Tag | NavigableString,
) -> tuple[str | None, str | None, str | None]:
    """
    Для получения:  Артикул, Название, Описание

    :param soup: суп из HTML-контента
    :return: tuple
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(name='div', attrs={'value': 'Description_0'})
    # Ищем весь блок Описание
    product_description_block = all_description_block.find(name='div', attrs={'text': 'Описание'})
    if product_description_block:
        # Берем нулевой div (название продукта)
        product_name_div = product_description_block.find_all('div')[0]
        product_name = product_name_div.get_text(
            separator=' ',
            strip=True
        ) if product_name_div else None

        # Берем первый div (артикул)
        product_id_div = product_description_block.find_all('div')[1]
        product_id = product_id_div.get_text(
            separator=' ',
            strip=True
        ) if product_id_div else None

        # Берем второй div (описание)
        product_description_div = product_description_block.find_all('div')[2]
        product_description = product_description_div.get_text(
            separator=' ',
            strip=True
        ) if product_description_div else None

        return (
            leave_numbers(clean_text_2(product_id.split(':')[1])),
            clean_text_2(product_name),
            clean_text_2(product_description)
        )

    return None, None, None


def get_img_link_in_base(
        product_title: str,
        product_id: str,
        image_dir_path: str,
        img_format: str = 'jpg',
) -> str:
    """
    Для получения Ссылка на изображение в базе

    :param product_title: исходное имя продукта
    :param product_id: str: артикул продукта
    :param image_dir_path: папка для сохранения изображения
    :param img_format: формат изображения
    :return: путь до изображения
    """
    cleaned_product_title = clean_product_name(product_title)
    image_path = Path(image_dir_path) / f'{cleaned_product_title}_{product_id}.{img_format}'
    return str(image_path)


def get_application_instruction(
        soup: Tag | NavigableString,
) -> str | None:
    """
    Для получения:  Применение

    :param soup: суп из HTML-контента
    :return: str
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(
        name='div',
        attrs={'value': 'Description_0'}
    )
    # Ищем весь блок Применение
    application_instruction_block = all_description_block.find(
        name='div',
        attrs={'text': 'Применение'}
    )
    if application_instruction_block:
        # Берем нулевой div (Применение продукта)
        application_instruction_div = application_instruction_block.find_all('div')[0]
        application_instruction = application_instruction_div.get_text(
            separator=' ', strip=True
        ) if application_instruction_div else None
        return clean_text_2(application_instruction)
    return None


def get_compound(
        soup: Tag | NavigableString,
) -> str | None:
    """
    Для получения:  Cостав

    :param soup: суп из HTML-контента
    :return: str
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(name='div', attrs={'value': 'Description_0'})
    # Ищем весь блок Cостав
    compound_block = all_description_block.find(name='div', attrs={'text': 'Состав'})
    if compound_block:
        # Берем нулевой div (Cостав продукта)
        compound_div = compound_block.find_all('div')[0]
        compound = compound_div.get_text(
            separator=' ', strip=True
        ) if compound_div else None
        return clean_text_2(compound)
    return None


def get_brand(
        soup: Tag | NavigableString,
) -> tuple[str | None, str | None, str | None]:
    """
    Для получения:  Бренд, Страна бренда, Описание бренда

    :param soup: суп из HTML-контента
    :return: str
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(name='div', attrs={'value': 'Description_0'})
    # Ищем весь блок Бренд
    brend_block = all_description_block.find(name='div', attrs={'text': 'Бренд'})
    if brend_block:
        # Берем нулевой div (Бренд продукта)
        brand_name_div = brend_block.find_all('div')[0]
        brand_name = brand_name_div.get_text(separator=' ', strip=True) if brand_name_div else None
        # Берем перый div (Страна продукта)
        brand_country_div = brend_block.find_all('div')[1]
        brand_country = brand_country_div.get_text(
            separator=' ',
            strip=True
        ) if brand_country_div else None
        # Берем второй div (Описание бренда продукта)
        brand_description_div = brend_block.find_all('div')[2]
        brand_description = brand_description_div.get_text(
            separator=' ',
            strip=True
        ) if brand_description_div else None
        return (
            clean_text_2(brand_name),
            clean_text_2(brand_country),
            clean_text_2(brand_description)
        )
    return None, None, None


def get_additional_info(
        soup: Tag | NavigableString,
) -> str | None:
    """
    Для получения:  Дополнительная информация

    :param soup: суп из HTML-контента
    :return: str
    """

    # Ищем весь блок Description_0
    all_description_block = soup.find(
        name='div',
        attrs={'value': 'Description_0'}
    )
    # Ищем весь блок Cостав
    additional_info_block = all_description_block.find(
        name='div',
        attrs={'text': 'Дополнительная информация'}
    )
    if additional_info_block:
        # Берем нулевой div (Дополнительная информация)
        additional_info_div = additional_info_block.find_all('div')[0]
        additional_info = additional_info_div.get_text(
            separator=' ', strip=True
        ) if additional_info_div else None
        return clean_text_2(additional_info)
    return None


def get_measure(characteristics: dict) -> tuple:
    """
    Для получения:  Мера, Юниты меры

    :param characteristics: характеристикаи товара.
    Последним ключом должно быть {....'вес': '50 г'}
    или  {....'объём': '250 мл'}

    :return: tuple
    """

    keys_to_check = ("вес", "объем", "объём")

    measure = next((key for key in keys_to_check if key in characteristics), None)

    if measure:
        measure_quantity, measure_units = characteristics.get(measure).split()
        return measure, measure_units, measure_quantity
    return None, None, None


def get_price_in_stock(
        soup: Tag | NavigableString,
) -> int | None:
    """
    Для получения:  Цена без скидки

    :param soup: суп из HTML-контента
    :return: int
    """

    # Ищем блок с ценой без скидки
    discount_div = soup.find("div", string=lambda text: text and "без скидки" in text)
    if discount_div:
        # Поднимаемся к родителю (это div, содержащий цену)
        parent_div = discount_div.find_parent("div")
        # Ищем внутри него div с ценой
        price_div = parent_div.find("div")
        price_str = price_div.get_text(separator=' ', strip=True) if price_div else None
        return int(re.sub(r"\D", "", price_str))

    if "по максимальной карте" in soup.get_text():
        return get_price_in_stock_by_max_card(soup=soup)

    return get_price_with_out_variance(soup=soup)


def get_price_with_out_variance(
        soup: Tag | NavigableString,
) -> int | None:
    """
    Для получения:  Цена без скидки когда только один вариант цены.

    :param soup: суп из HTML-контента
    :return: int
    """

    # Ищем блок с ценой
    discount_div = soup.find_all(
        name="meta",
        attrs={
            "itemprop": "availability",
            "href": "http://schema.org/InStock",
        }
    )
    if discount_div:
        # Поднимаемся к родителю (это div, содержащий цену)
        parent_div = discount_div[0].find_parent("div")
        if parent_div:
            price_div = parent_div.find(
                name="meta",
                attrs={
                    "itemprop": "price",
                }
            )
            if price_div:
                return int(price_div['content'])

    return None


def get_price_in_stock_by_max_card(
        soup: Tag | NavigableString,
) -> int | None:
    """
    Для получения:  Цена без скидки со словами "по максимальной карте"

    :param soup: суп из HTML-контента
    :return: int
    """

    # Ищем блок с "по максимальной карте"
    max_card_div = soup.find("div", string=lambda text: text and "по максимальной карте" in text)
    # Поднимаемся к родителю два раза (это div, содержащий цену)
    parent_div = max_card_div.find_parent("div").find_parent("div")
    price_div = parent_div.find_all("meta", attrs={"itemprop": "price"})

    if price_div:
        return int(price_div[0]['content'])

    return None


def get_img_link(
        soup: Tag | NavigableString,
) -> str | None:
    """
    Для получения:  Ссылки на изображение

    :param soup: суп из HTML-контента
    :return: int
    """

    # Ищем блок с ссылкой
    img_gallery_block = soup.find_all(
        name='picture',
        attrs={
            'class': "ga-image-responsive",
            'name': "gallery-preview",
        })
    # print(img_gallery_block)

    for picture in img_gallery_block:
        # Ищем первый тег <img> внутри <picture>
        img_tag = picture.find('img', src=True)
        link = img_tag['src']
        if link and (link.endswith('.jpg')) and ('video' not in link):
            return img_tag['src']  # Возвращаем первую jpg-картинку

    return get_img_link_if_one_img(soup)


def get_img_link_if_one_img(
        soup: Tag | NavigableString,
) -> str | None:
    """
    Для получения:  Ссылки на изображение, если изображение без галереи

    :param soup: суп из HTML-контента
    :return: int
    """

    # Ищем блок с ссылкой
    img_gallery_block = soup.find_all(
        name='source',
        attrs={
            'media': "(min-width: 1920px)",
        })

    for source in img_gallery_block:
        if source['srcset'].endswith('.jpg'):
            return source['srcset']  # Возвращаем первую jpg-картинку

    return None
