from pathlib import Path

from pdf.pdf_data_processing.tasks_utils import (
    calculate_price_per_standard_unit,
    get_brand_line_path,
)


def analysis_composition_one_product_task_main(
        collection_data: dict,
        info_data: dict,
        rus_product_data_dict: dict,
        product_name: str,
) -> dict:
    """
    Задача "Разбор состава одного средства"

    :param collection_data: данные подборки
    :param info_data: данные с всеми средствами, врачами и т.д.
    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :param product_name: наименование средства

    :return: словарь с специфичными данными по средству по задаче
    """

    data = {
        'Плюсы': rus_product_data_dict['Плюсы'],
        'Минусы': rus_product_data_dict['Минусы'],
        'Текстура': rus_product_data_dict['Текстура'],
        'Соотношение цены': calculate_price_per_standard_unit(
            quantity=info_data[product_name]['Количество меры (число)'],
            unit=info_data[product_name]['Юниты меры (мл/шт)'],
            price_rub=info_data[product_name]['Стоимость руб'],
        ),
        'Основные компоненты': rus_product_data_dict['Основные компоненты'],
        'Активные компоненты': rus_product_data_dict['Активные компоненты'],
        'Увлажняющие и ухаживающие компоненты': rus_product_data_dict['Увлажняющие и ухаживающие компоненты'],
        'Консерванты и регуляторы pH': rus_product_data_dict['Консерванты и регуляторы pH'],
        'Дополнительные компоненты': rus_product_data_dict['Дополнительные компоненты'],
        'Запрещенные или нежелательные компоненты': rus_product_data_dict['Запрещенные или нежелательные компоненты'],
        'Вывод': rus_product_data_dict['Вывод'],
        'Путь к изображению бренд-линии': Path(get_brand_line_path(
            task=collection_data['Задача'],
            category=collection_data['Категория'],
            brand_line_color='Цвет_1'
        )
        ),
    }

    additional_data = _get_category_additional_data(
        collection_data=collection_data,
        rus_product_data_dict=rus_product_data_dict,
    )

    if additional_data:
        data.update(additional_data)
    return data


def _get_category_additional_data(
        collection_data: dict,
        rus_product_data_dict: dict,
) -> dict | None:
    """
    Возвращает дополнительные данные в зависимости от категории,
    или None, если для этой категории дополнительных данных нет

    :param collection_data: данные подборки
    :param rus_product_data_dict: словарь с данными по средству с русскими ключами

    :return: словарь с специфичными данными
    """

    CATEGORY_WITH_ADDITIONAL_DATA = {
        "Уход за кожей лица": _category_facial_skin_care,
        "Уход за телом": _category_body_care,
        "Макияж": _category_makeup,
        "Парфюмерия": _category_perfumery,
        "Стайлинг волос": _category_hair_styling,
    }

    additional_data_func = CATEGORY_WITH_ADDITIONAL_DATA.get(
        collection_data['Категория'], None
    )
    if additional_data_func:
        return additional_data_func(
            rus_product_data_dict=rus_product_data_dict,
        )
    return None


def _category_hair_styling(
        rus_product_data_dict: dict,
) -> dict:
    """
    Задача "Разбор состава одного средства"
    дополнительные данные для категории "Стайлинг волос"

    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :return: словарь с специфичными данными
    """

    return {
        'Степень фиксации': rus_product_data_dict['Степень фиксации'],
        'Ощущение на волосах': rus_product_data_dict['Ощущение на волосах'],
    }


def _category_makeup(
        rus_product_data_dict: dict,
) -> dict:
    """
    Задача "Разбор состава одного средства"
    дополнительные данные для категории "Макияж"

    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :return: словарь с специфичными данными
    """

    return {
        'Стойкость': rus_product_data_dict['Стойкость'],
        'Финиш': rus_product_data_dict['Финиш'],
        'Пигментация': rus_product_data_dict['Пигментация'],
        'Покрытие': rus_product_data_dict['Покрытие'],
        'Водостойкость': rus_product_data_dict['Водостойкость'],
        'Уровень SPF': rus_product_data_dict['Уровень SPF'],
    }


def _category_body_care(
        rus_product_data_dict: dict,
) -> dict:
    """
    Задача "Разбор состава одного средства"
    дополнительные данные для категории "Уход за телом"

    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :return: словарь с специфичными данными
    """

    return {
        'Влияние на тип кожи': rus_product_data_dict['Влияние на тип кожи'],
        'Интенсивность пилинга': rus_product_data_dict['Интенсивность пилинга'],
        'Длительность защиты': rus_product_data_dict['Длительность защиты'],
        'Пенообразование': rus_product_data_dict['Пенообразование'],
    }


def _category_facial_skin_care(
        rus_product_data_dict: dict,
) -> dict:
    """
    Задача "Разбор состава одного средства"
    дополнительные данные для категории "Уход за кожей лица"

    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :return: словарь с специфичными данными
    """

    return {
        'Влияние на тип кожи': rus_product_data_dict['Влияние на тип кожи'],
        'Уровень SPF': rus_product_data_dict['Уровень SPF'],
        'Время нанесения': rus_product_data_dict['Время нанесения'],
        'Уровень pH': rus_product_data_dict['Уровень pH'],
        'Интенсивность пилинга': rus_product_data_dict['Интенсивность пилинга'],
        'Эффект на область глаз': rus_product_data_dict['Эффект на область глаз'],
    }


def _category_perfumery(
        rus_product_data_dict: dict,
) -> dict:
    """
    Задача "Разбор состава одного средства"
    дополнительные данные для категории "Парфюмерия"

    :param rus_product_data_dict: словарь с данными по средству с русскими ключами
    :return: словарь с специфичными данными
    """

    return {
        'Основные ноты': rus_product_data_dict['Основные ноты'],
        'Стойкость': rus_product_data_dict['Стойкость'],
        'Раскрытие аромата': rus_product_data_dict['Раскрытие аромата'],
    }
