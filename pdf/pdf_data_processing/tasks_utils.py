from source.pdf_structure_mapping import PDF_SETTINGS


def get_brand_line_path(
        task: str,
        brand_line_color: str
) -> str:
    """
    :param task: код задачи
    :param brand_line_color: ключ цвета

    Возвращает путь к файлу с нужной бренд-линией для нанесения
    на PDF в зависимости от задачи
    """

    return PDF_SETTINGS[task]['Пути бренд-линий'][brand_line_color]


def get_brand_line_sizes(
        task: str,
) -> str:
    """
    :param task: код задачи

    Возвращает размеры бренд-линии для нанесения
    на PDF в зависимости от задачи
    """

    return PDF_SETTINGS[task]['Размеры бренд-линии']


def get_pdf_flowables(
        task: str,
) -> dict:
    """
    :param task: код задачи

    Возвращает словарь с flowables-элементами pdf-документа
    """

    return PDF_SETTINGS[task]['Элементы и стили']


def get_pdf_doc_sizes(
        task: str,
) -> tuple:
    """
    :param task: код задачи

    Возвращает кортеж с размерами pdf-документа
    """

    return PDF_SETTINGS[task]['Размеры документа']


def get_pdf_page_templates(
        task: str,
) -> dict:
    """
    :param task: код задачи

    Возвращает dict с данными по шаблонами страниц с фреймами
    """

    return PDF_SETTINGS[task]['Шаблоны страниц с фреймами']
