from pathlib import Path
from types import MappingProxyType

from source.pdf_structure_mapping import get_pdf_structure
from source.structure_for_products import MAPPING_KEYS

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
        f'{product.get("Юниты меры (мл/шт)")} / {product.get("Стоимость руб")} рублей'
    )


def get_brand_line_path(
        task: str,
        category: str,
        brand_line_color: str
) -> str:
    """
    :param task: код задачи
    :param category: категория подборки
    :param brand_line_color: ключ цвета

    Возвращает путь к файлу с нужной бренд-линией для нанесения
    на PDF в зависимости от задачи
    """
    pdf_structure = get_pdf_structure(
        task=task,
        category=category,
    )
    return pdf_structure['Пути бренд-линий'][brand_line_color]


def get_brand_line_sizes(
        task: str,
        category: str,
) -> str:
    """
    :param task: код задачи
    :param category: категория подборки

    Возвращает размеры бренд-линии для нанесения
    на PDF в зависимости от задачи
    """

    pdf_structure = get_pdf_structure(
        task=task,
        category=category,
    )
    return pdf_structure['Размеры бренд-линии']


def get_pdf_flowables(
        task: str,
        category: str,
) -> dict:
    """
    :param task: код задачи
    :param category: категория подборки

    Возвращает словарь с flowables-элементами pdf-документа
    """
    pdf_structure = get_pdf_structure(
        task=task,
        category=category,
    )
    return pdf_structure['Элементы и стили']


def get_pdf_doc_sizes(
        task: str,
        category: str,
) -> tuple:
    """
    :param task: код задачи
    :param category: категория подборки

    Возвращает кортеж с размерами pdf-документа
    """

    pdf_structure = get_pdf_structure(
        task=task,
        category=category,
    )
    return pdf_structure['Размеры документа']


def get_pdf_page_templates(
        task: str,
        category: str,
) -> dict:
    """
    :param task: код задачи
    :param category: категория подборки

    Возвращает dict с данными по шаблонами страниц с фреймами
    """

    pdf_structure = get_pdf_structure(
        task=task,
        category=category,
    )
    return pdf_structure['Шаблоны страниц с фреймами']


def format_product_filename(
        product_title: str,
        path_to_output_folder_pdf_file: str,
) -> Path:
    """
    Возвращает полный путь для сохранения файла .pdf

    :param path_to_output_folder_pdf_file: путь (Path) к папке для сохранения PDF.
    :param product_title: наименование средства

    :return: полный путь к файлу PDF
    """

    output_folder_pdf = Path(path_to_output_folder_pdf_file)
    safe_filename = product_title.replace(" ", "_").replace("/", "_").lower() + ".pdf"

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
        "гр": ("гр", 1)
    }


    if unit in conversion_factors:
        base_unit, factor = conversion_factors[unit]
        base_quantity = quantity * factor
    else:
        raise ValueError(f"Неизвестная единица измерения: {unit}")

    # Определяем стандартное количество
    standard_quantity = 100 if base_quantity >= 100 else 50

    # Рассчитываем цену за стандартное количество
    price_per_standard = (price_rub / base_quantity) * standard_quantity
    return f'{standard_quantity} {base_unit} / {int(price_per_standard)} р.'


def mapping_keys_to_rus(
        data: dict,
        mapping:  MappingProxyType = MAPPING_KEYS,
) -> dict:
    """
    Заменяет ключи в словаре `data` на русские аналоги из `mapping`, если они есть.

    :param data: Исходный словарь с данными.
    :param mapping: Словарь с соответствием новых ключей.
    :return: Новый словарь с изменёнными ключами.
    """
    return {mapping.get(k, k): v for k, v in data.items()}
