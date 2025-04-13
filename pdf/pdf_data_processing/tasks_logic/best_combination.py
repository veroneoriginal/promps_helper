# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Лучшее сочетание'
"""
from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import (
    get_path_for_save_pdf,
)
from source.structure_folders import (
    GREEN_ACCEPT_CHECK_IMAGE_PATH,
    GREEN_VERTICAL_BRAND_LINE_PATH,
    FIOLET_VERTICAL_BRAND_LINE_PATH,
)

PDF_STRUCTURE = {
    'Исходное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 0, 'y': 666,
              'font_name': 'Montserrat-Regular',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': 0, 'y': 54,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('FreeImage',
             {
                 'Ключ в подборке': 'Путь к изображению галочки',
                 'x': 620,
                 'y': 450,
                 'width': 225,
                 'height': 225,
                 'preserve_aspect_ratio': True,
             }
             ),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BC_normal_1'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BC_normal_1'}),

        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
    'Подобранное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 0, 'y': 666,
              'font_name': 'Montserrat-Regular',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': 0, 'y': 54,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('FreeImage',
             {
                 'Ключ в подборке': 'Путь к изображению галочки',
                 'x': 620,
                 'y': 450,
                 'width': 225,
                 'height': 225,
                 'preserve_aspect_ratio': True,
             }
             ),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 54}),
            ('Paragraph', {'Текст': '<b>Почему выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
    'Невыбранное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 0, 'y': 666,
              'font_name': 'Montserrat-Regular',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': 0, 'y': 54,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 54}),
            ('Paragraph', {'Текст': '<b>Почему НЕ выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
}


class BestCombinationProductPDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Лучшее сочетание"
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
        Задача "Лучшее сочетание"
        :return: Возвращает список с данными для создания документов
        """

        source_product_template = self.get_source_product_template(
            one_product_data=self.rus_selection_result['Исходное_средство']
        )
        self.pdf_docs_data.append(source_product_template)

        other_templates = self.get_other_templates(all_data=self.rus_selection_result)

        self.pdf_docs_data.extend(other_templates)

        return self.pdf_docs_data

    def get_other_templates(
            self,
            all_data: dict
    ) -> list:
        """
        Наполняет шаблоны с выбранным средством и невыбранными средствами.
        :param all_data: данные со всеми средствами
        :return: список с шаблонами
        """
        templates = []

        for key, data in all_data.items():
            if key.startswith('product_'):
                if data['Лучшее средство']:
                    best_combination_product_template = self.get_best_combination_product_template(
                        one_product_data=data
                    )
                    templates.append(best_combination_product_template)
                else:
                    unselected_combination_product_template = self.get_unselected_combination_product_template(
                        one_product_data=data
                    )
                    templates.append(unselected_combination_product_template)
        return templates

    def get_unselected_combination_product_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет шаблон с невыбранным средством
        :param one_product_data: данные одного средства
        :return: шаблон
        """

        product_name = one_product_data['Название средства']
        product_article = one_product_data['Артикул в Золотом Яблоке']

        unselected_combination_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data = {
            # исходное средство
            'Вывод': one_product_data['Вывод'],
            'Путь к изображению бренд-линии': FIOLET_VERTICAL_BRAND_LINE_PATH,
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            ),
        }

        template_data.update(PDF_STRUCTURE['Невыбранное средство'])
        template_data.update(unselected_combination_product_data)

        return template_data

    def get_best_combination_product_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет шаблон с лучшим средством PDF
        """

        product_name = one_product_data['Название средства']
        product_article = one_product_data['Артикул в Золотом Яблоке']

        best_combination_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data = {
            # исходное средство
            'Вывод': one_product_data['Вывод'],
            'Путь к изображению бренд-линии': GREEN_VERTICAL_BRAND_LINE_PATH,
            'Путь к изображению галочки': GREEN_ACCEPT_CHECK_IMAGE_PATH,
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            ),
        }

        template_data.update(PDF_STRUCTURE['Подобранное средство'])
        template_data.update(best_combination_product_data)

        return template_data

    def get_source_product_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет шаблон PDF для исходного средства
        :param one_product_data: данные одного средства
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = one_product_data['Название средства']
        product_article = one_product_data['Артикул в Золотом Яблоке']

        base_source_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data = {
            # исходное средство
            'Плюсы': one_product_data['Плюсы'],
            'Минусы': one_product_data['Минусы'],
            'Путь к изображению бренд-линии': GREEN_VERTICAL_BRAND_LINE_PATH,
            'Путь к изображению галочки': GREEN_ACCEPT_CHECK_IMAGE_PATH,
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            ),
        }

        template_data.update(PDF_STRUCTURE['Исходное средство'])
        template_data.update(base_source_product_data)

        return template_data
