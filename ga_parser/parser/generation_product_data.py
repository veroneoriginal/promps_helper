from ga_parser.utils.utils import (
    clean_value_str_in_dict,
    list_to_dict,
    create_full_link_to_image,
    calculate_price_ml,
)


def get_product_data_dict(product_card: dict) -> dict:
    """
    Формирования финального словаря со всеми данными по средству

    :param product_card: карточка средства в виде словаря
    :return: dict
    """

    (
        item_in_shop,
        product_title,
        product_description,
    ) = get_item_title_description(product_card)
    (
        product_type,
        for_whom,
        purpose,
        hair_type,
        skin_type,
        scope_of_application
    ) = get_attributes(product_card)
    (
        brand_name,
        brand_country,
        brand_description,
    ) = get_brand(product_card)
    (
        measure,
        measure_units,
    ) = get_measure(product_card)

    additional_info = get_additional_info(product_card)
    application_instruction = get_application_instruction(product_card)
    compound = get_compound(product_card)
    measure_quantity = get_measure_quantity(product_card)
    price = get_price_by_units(product_card, measure_quantity)
    img_link = get_img_link(product_card, measure_quantity)
    cost_for_comparison = calculate_price_ml(measure_quantity, price)

    data = {
        'Артикул в Золотом Яблоке': item_in_shop,
        'Название': product_title,
        'Описание': product_description,
        'Тип продукта': product_type,
        'Для кого': for_whom,
        'Назначение': purpose,
        'Тип волос': hair_type,
        'Тип кожи': skin_type,
        'Область применения': scope_of_application,
        'Мера (объём/количество)': measure,
        'Количество меры (число)': measure_quantity,
        'Юниты меры (мл/шт)': measure_units,
        'Стоимость руб': price,
        'Стоимость за 100 мл руб': cost_for_comparison,
        'Применение': application_instruction,
        'Состав': compound,
        'Бренд': brand_name,
        'Ссылка на изображение': img_link,
        'Страна бренда': brand_country,
        'Описание бренда': brand_description,
        'Дополнительная информация': additional_info,
        'Заполнено': 'да',
    }

    return clean_value_str_in_dict(data)


def _get_product_description(_product_card: dict) -> dict:
    """
    Для получения вложенного словаря по ключу 'productDescription'
    Пример словаря карточки средства в модуле example_product_card_dict.py

    :param _product_card: карточка средства в виде словаря
    :return: dict
    """

    return _product_card.get('productDescription')


def get_item_title_description(_product_card: dict) -> tuple:
    """
    Для получения:  Артикул, Название, Описание

    :param _product_card: карточка средства в виде словаря
    :return: tuple
    """
    description_dict = _get_product_description(_product_card)[0]

    item_in_shop = _product_card.get('id')
    product_title = description_dict.get('title')
    product_description = description_dict.get('content')

    return item_in_shop, product_title, product_description


def get_attributes(_product_card: dict) -> tuple:
    """
    Для получения: Тип продукта, Для кого, Назначение, Тип волос,
    Тип кожи, Область применения

    :param _product_card: карточка средства в виде словаря
    :return: tuple
    """

    attributes_dict = list_to_dict(_get_product_description(_product_card)[0].get("attributes"))

    product_type = attributes_dict.get('тип продукта')
    for_whom = attributes_dict.get('для кого')
    purpose = attributes_dict.get('назначение')
    hair_type = attributes_dict.get('тип волос')
    skin_type = attributes_dict.get('тип кожи')
    scope_of_application = attributes_dict.get('область применения')

    return (
        product_type,
        for_whom,
        purpose,
        hair_type,
        skin_type,
        scope_of_application
    )


def get_application_instruction(_product_card: dict) -> str:
    """
    Для получения:  Применение

    :param _product_card: карточка средства в виде словаря
    :return: str
    """

    return _get_product_description(_product_card)[1].get('content')


def get_compound(_product_card: dict) -> str:
    """
    Для получения:  Cостав

    :param _product_card: карточка средства в виде словаря
    :return: str
    """

    return _get_product_description(_product_card)[2].get('content')


def get_brand(_product_card: dict) -> tuple:
    """
    Для получения:  Бренд, Страна бренда, Описание бренда

    :param _product_card: карточка средства в виде словаря
    :return: tuple
    """

    info = _get_product_description(_product_card)[3]
    brand_name = info.get('title')
    brand_country = info.get('subtitle')
    brand_description = info.get('content')

    return brand_name, brand_country, brand_description


def get_additional_info(_product_card: dict) -> str:
    """
    Для получения:  Дополнительная информация

    :param _product_card: карточка средства в виде словаря
    :return: str
    """

    return _get_product_description(_product_card)[4].get('content')


def get_measure(_product_card: dict) -> tuple:
    """
    Для получения Мера, Юниты меры

    :param _product_card: карточка средства в виде словаря
    :return: tuple
    """
    attr = _product_card.get('attributes').get('units')
    measure = attr.get('label')
    measure_units = attr.get('unit')
    return measure, measure_units


def get_measure_quantity(_product_card: dict) -> str:
    """
    Для получения Количество меры

    :param _product_card: карточка средства в виде словаря
    :return: str
    """
    return _product_card.get('attributesSelectedDefault').get('units')


def get_price_by_units(_product_card, units: str) -> int | float | None:
    """
    Возвращает цену из поля "regular" для элемента,
    у которого значение "units" соответствует переданному числу.

    :param _product_card: карточка средства в виде словаря
    :param units: значение units для поиска
    :return: цена из поля "regular" или None, если не найдено
    """

    data = _product_card.get('variants')

    for item in data:
        if item.get("attributesValue", {}).get("units", 0) == units:
            return item.get("price", {}).get("regular", {}).get("amount")
    return None


def get_img_link(_product_card, units: str) -> str | None:
    """
    Для получения Ссылка на img

    :param _product_card: карточка средства в виде словаря
    :param units: значение units для поиска
    :return: str
    """
    data = _product_card.get('variants')
    for item in data:
        if item.get("attributesValue", {}).get("units", 0) == units:
            link = item.get("imageUrls", {})[0].get("url", {})
            return create_full_link_to_image(link)
    return None
