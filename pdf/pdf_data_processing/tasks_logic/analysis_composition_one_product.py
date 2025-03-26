# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Разбор состава одного средства'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import format_product_filename, calculate_price_per_standard_unit

ADDITIONAL_ELEMENTS_BY_PRODUCT_CATEGORY = {
    "Уход за кожей лица": [
        ('Paragraph', {'Текст': '<b>Влияние на тип кожи:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Влияние на тип кожи', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень SPF:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Уровень SPF', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Время нанесения:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Время нанесения', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень pH:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Уровень pH', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Интенсивность пилинга:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Интенсивность пилинга', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Эффект на область глаз:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Эффект на область глаз', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Уход за телом': [
        ('Paragraph', {'Текст': '<b>Влияние на тип кожи:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Влияние на тип кожи', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Интенсивность пилинга:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Интенсивность пилинга', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Длительность защиты:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Длительность защиты', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Пенообразование:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Пенообразование', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Макияж': [
        ('Paragraph', {'Текст': '<b>Стойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Стойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Финиш:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Финиш', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Пигментация:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Пигментация', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Покрытие:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Покрытие', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Водостойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Водостойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень SPF:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Уровень SPF', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Парфюмерия': [
        ('Paragraph', {'Текст': '<b>Основные ноты:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Основные ноты', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Стойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Стойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Раскрытие аромата:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Раскрытие аромата', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Стайлинг волос': [
        ('Paragraph', {'Текст': '<b>Степень фиксации:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Степень фиксации', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Ощущение на волосах:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 10}),
        ('Paragraph', {'Ключ в подборке': 'Ощущение на волосах', 'Стиль': 'ACOP_normal_3'}),
    ],
}

PDF_STRUCTURE = {
    'Базовая категория': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 25}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
              'font_name': 'DejaVuSans',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
              'font_name': 'DejaVuSans',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Текст': '<b>Разбор состава</b>', 'Стиль': 'ACOP_title_2'}),
            ('Spacer', {'width': 1, 'height': 30}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'ACOP_normal_2'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'ACOP_title_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Цена за средство:</b>', 'Стиль': 'ACOP_bold_2'}),
            ('Spacer', {'width': 1, 'height': 25}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'ACOP_base_price_1'}),
            ('Spacer', {'width': 1, 'height': 40}),
            ('Paragraph', {'Текст': '<b>Соотношение цены:</b>', 'Стиль': 'ACOP_bold_2'}),
            ('Spacer', {'width': 1, 'height': 25}),
            ('Paragraph', {'Ключ в подборке': 'Соотношение цены', 'Стиль': 'ACOP_price_ratio_1'}),
            ('NextPageTemplate', {'template_id': 'template_2'}),
            ('PageBreak', {}),
            # следующая страница
            ('Paragraph', {'Текст': '<b>Основные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph', {'Ключ в подборке': 'Основные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Активные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph', {'Ключ в подборке': 'Активные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph',
             {'Текст': '<b>Увлажняющие и ухаживающие компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph',
             {'Ключ в подборке': 'Увлажняющие и ухаживающие компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Консерванты и регуляторы pH:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph', {'Ключ в подборке': 'Консерванты и регуляторы pH', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Дополнительные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph',
             {'Ключ в подборке': 'Дополнительные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph',
             {'Текст': '<b>Запрещенные или нежелательные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph',
             {'Ключ в подборке': 'Запрещенные или нежелательные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph',
             {'Ключ в подборке': 'Плюсы', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'ACOP_normal_3'}),
            # Сюда вставим дополнительную информацию по категории индекс -4
            ('Paragraph', {'Текст': '<b>Вывод:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'ACOP_normal_3'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (100, 0), (596, 966)),
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
            'template_2':
                (
                    (0, (100, 80), (596, 820)),
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                )

        },

    },

}


class AnalisisCompositionProductPDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Разбор состава одного средства"
    """

    def __init__(
            self,
            collection_data: dict,
            info_data: dict,
            rus_selection_result: dict,
            path_to_output_folder_pdf_file: str
    ):
        """
        :param collection_data: данные подборки
        :param info_data: данные с всеми средствами, врачами и т.д.
        :param rus_selection_result: словарь с данными по средству с русскими ключами
        :param path_to_output_folder_pdf_file: путь к папке для сохранения pdf-файлов
        """
        self.collection_data = collection_data
        self.info_data = info_data
        self.rus_selection_result = rus_selection_result
        self.path_to_output_folder_pdf_file = path_to_output_folder_pdf_file
        self.pdf_docs_data = []

    # pylint: disable=W0613 unused-argument
    def get_data_for_pdf_docs(self) -> list:
        """
        Задача "Разбор состава одного средства"
        :return: Возвращает список с данными для создания документов
        """

        template = self.get_base_template()
        self.pdf_docs_data.append(template)

        return self.pdf_docs_data

    def get_additional_product_data_by_category(self) -> dict | None:
        """
        Возвращает дополнительную информацию в зависимости от
        категории подборки ("Стайлинг волос", "Макияж" и т.д.)
        """

        CATEGORY_WITH_ADDITIONAL_DATA = {
            "Уход за кожей лица": self._category_facial_skin_care,
            "Уход за телом": self._category_body_care,
            "Макияж": self._category_makeup,
            "Парфюмерия": self._category_perfumery,
            "Стайлинг волос": self._category_hair_styling,
        }

        additional_data_func = CATEGORY_WITH_ADDITIONAL_DATA.get(
            self.collection_data['Категория'], None
        )

        if additional_data_func:
            return additional_data_func()
        return None

    def get_base_template(self) -> dict:
        """
        Наполняет базовый шаблон PDF
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = self.rus_selection_result['Название средства']
        product_data = self.info_data['Средства'][product_name]

        template_data = {  # отличается:
            'Плюсы': self.rus_selection_result['Плюсы'],
            'Минусы': self.rus_selection_result['Минусы'],
            'Текстура': self.rus_selection_result['Текстура'],
            'Соотношение цены': calculate_price_per_standard_unit(
                quantity=product_data['Количество меры (число)'],
                unit=product_data['Юниты меры (мл/шт)'],
                price_rub=product_data['Стоимость руб'],
            ),
            'Путь к изображению бренд-линии': Path("00_base/source/imagine_border/border_green.jpg"),
            'Путь для сохранения pdf-файла': Path(format_product_filename(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file),
            ),
            'Основные компоненты': self.rus_selection_result['Основные компоненты'],
            'Активные компоненты': self.rus_selection_result['Активные компоненты'],
            'Увлажняющие и ухаживающие компоненты': self.rus_selection_result['Увлажняющие и ухаживающие компоненты'],
            'Консерванты и регуляторы pH': self.rus_selection_result['Консерванты и регуляторы pH'],
            'Дополнительные компоненты': self.rus_selection_result['Дополнительные компоненты'],
            'Запрещенные или нежелательные компоненты': self.rus_selection_result[
                'Запрещенные или нежелательные компоненты'],
            'Вывод': self.rus_selection_result['Вывод'],
        }

        base_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
        )

        template_data.update(base_product_data)
        template_data.update(PDF_STRUCTURE['Базовая категория'])

        # Добавляем дополнительные данные по категории
        additional_data = self.get_additional_product_data_by_category()
        if additional_data:
            template_data.update(additional_data)
            # Добавляем в структуру шаблона дополнительные блоки
            # в зависимости от категории продукта
            additional_block = ADDITIONAL_ELEMENTS_BY_PRODUCT_CATEGORY[
                self.collection_data['Категория']
            ]

            template_data['Элементы и стили'][-3:-3] = additional_block

        return template_data

    def _category_hair_styling(self) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Стайлинг волос"

        :return: словарь с специфичными данными
        """

        return {
            'Степень фиксации': self.rus_selection_result['Степень фиксации'],
            'Ощущение на волосах': self.rus_selection_result['Ощущение на волосах'],
        }

    def _category_makeup(self) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Макияж"

        :return: словарь с специфичными данными
        """

        return {
            'Стойкость': self.rus_selection_result['Стойкость'],
            'Финиш': self.rus_selection_result['Финиш'],
            'Пигментация': self.rus_selection_result['Пигментация'],
            'Покрытие': self.rus_selection_result['Покрытие'],
            'Водостойкость': self.rus_selection_result['Водостойкость'],
            'Уровень SPF': self.rus_selection_result['Уровень SPF'],
        }

    def _category_body_care(self) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за телом"

        :return: словарь с специфичными данными
        """

        return {
            'Влияние на тип кожи': self.rus_selection_result['Влияние на тип кожи'],
            'Интенсивность пилинга': self.rus_selection_result['Интенсивность пилинга'],
            'Длительность защиты': self.rus_selection_result['Длительность защиты'],
            'Пенообразование': self.rus_selection_result['Пенообразование'],
        }

    def _category_facial_skin_care(self) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за кожей лица"

        :return: словарь с специфичными данными
        """

        return {
            'Влияние на тип кожи': self.rus_selection_result['Влияние на тип кожи'],
            'Уровень SPF': self.rus_selection_result['Уровень SPF'],
            'Время нанесения': self.rus_selection_result['Время нанесения'],
            'Уровень pH': self.rus_selection_result['Уровень pH'],
            'Интенсивность пилинга': self.rus_selection_result['Интенсивность пилинга'],
            'Эффект на область глаз': self.rus_selection_result['Эффект на область глаз'],
        }

    def _category_perfumery(self) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Парфюмерия"

        :return: словарь с специфичными данными
        """

        return {
            'Основные ноты': self.rus_selection_result['Основные ноты'],
            'Стойкость': self.rus_selection_result['Стойкость'],
            'Раскрытие аромата': self.rus_selection_result['Раскрытие аромата'],
        }
