import re
from pathlib import Path
from types import MappingProxyType

from source.structure_for_products import MAPPING_KEYS


def capitalize_first_letter(text: str) -> str:
    """
    Сделать первую букву заглавной
    """
    for i, char in enumerate(text):
        if char.isalpha():
            return text[:i] + char.upper() + text[i + 1:]
    return text  # если букв вообще нет


def extract_product_name(title: str) -> str:
    """
    Удаляет из строки (артикул: 123456)
    """
    return re.sub(r"\s*\(артикул:.*?\)", "", title, flags=re.IGNORECASE).strip()


def calc_base_price_ratio(
        product: dict,
) -> str:
    """
    Готовит строку 'Количество мера / цена'
    Например: '190 мл / 1612 р.'

    :param product: словарь с информацией по одному средству
    :return: str
    """

    return (
        f'{product.get("Количество меры (число)")} '
        f'{product.get("Юниты меры (мл/шт)")} / {product.get("Стоимость руб")} руб'
    )


def get_path_for_save_pdf(
        product_title: str,
        path_to_output_folder_pdf_file: str,
        product_article: str,
) -> Path:
    """
    Возвращает полный путь для сохранения файла .pdf

    :param path_to_output_folder_pdf_file: путь (Path) к папке для сохранения PDF.
    :param product_title: наименование средства
    :param product_article: Артикул средства в Золотом Яблоке

    :return: полный путь к файлу PDF
    """
    output_folder_pdf = Path(path_to_output_folder_pdf_file)

    # Удаляем всё, кроме букв (латиница, кириллица), цифр и подчёркиваний
    safe_name = re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9]+", "_", product_title.strip().lower())

    safe_filename = f'{safe_name}_{product_article}.pdf'
    return output_folder_pdf / safe_filename


def calculate_price_per_standard_unit(
        quantity: str,
        unit: str,
        price_rub: int | float,
) -> str:
    """
    Рассчитывает стоимость за стандартный объем (100 или 50) в зависимости
    от количества и единицы измерения.

    :param quantity: Количество меры (например, 250, 50, 2)
    :param unit: Юниты меры (например, "мл", "гр", "л")
    :param price_rub: Стоимость в рублях

    :return: строку с информацией о стоимости за стандартное
    количество (100 или 50) с учётом единицы измерения.
    """
    quantity = int(quantity)

    # Конвертация в базовые единицы
    conversion_factors = {
        "л": ("мл", 1000),  # 1 л = 1000 мл
        "кг": ("гр", 1000),  # 1 кг = 1000 гр
        "мл": ("мл", 1),
        "гр": ("гр", 1),
        "г": ("г", 1),
    }

    if unit in conversion_factors:
        base_unit, factor = conversion_factors[unit]
        base_quantity = quantity * factor
    else:
        raise ValueError(f"Неизвестная единица измерения: {unit}")

    # Выбор стандартного количества:
    if base_quantity <= 50:
        standard_quantity = 10
    elif base_quantity < 100:
        standard_quantity = 50
    else:
        standard_quantity = 100

    # Рассчитываем цену за стандартное количество
    price_per_standard = (price_rub / base_quantity) * standard_quantity
    return f'{standard_quantity} {base_unit} / {int(price_per_standard)} р.'


def translate_keys_to_rus(
        data: dict,
        mapping: MappingProxyType = MAPPING_KEYS,
) -> dict:
    """
    Заменяет ключи в словаре `data` на русские аналоги из `mapping`, если они есть.

    :param data: Исходный словарь с данными.
    :param mapping: Словарь с соответствием новых ключей.
    :return: Новый словарь с изменёнными ключами.
    """
    if isinstance(data, dict):
        return {
            mapping.get(key, key): translate_keys_to_rus(value, mapping)
            for key, value in data.items()
        }
    return data
