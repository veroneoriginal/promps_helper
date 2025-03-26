# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Лучшее сочетание'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import (
    format_product_filename,
)

PDF_STRUCTURE = {
    'Исходное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
              'font_name': 'DejaVuSans',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
              'font_name': 'DejaVuSans',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 15}),
            ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BC_normal_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 15}),
            ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BC_normal_1'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (100, 0), (596, 966)),
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
    'Подобранное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
              'font_name': 'DejaVuSans',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
              'font_name': 'DejaVuSans',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 40}),
            ('Paragraph', {'Текст': '<b>Почему выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 15}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (100, 0), (596, 966)),
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
    'Невыбранное средство': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 10}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
              'font_name': 'DejaVuSans',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
              'font_name': 'DejaVuSans',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
            ('Spacer', {'width': 1, 'height': 40}),
            ('Paragraph', {'Текст': '<b>Почему НЕ выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
            ('Spacer', {'width': 1, 'height': 15}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (100, 0), (596, 966)),
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

        source_product_template = self.get_source_product_template()
        self.pdf_docs_data.append(source_product_template)
        best_combination_product_template = self.get_best_combination_product_template()
        self.pdf_docs_data.append(best_combination_product_template)
        unselected_combination_product_template = self.get_unselected_combination_product_template()
        self.pdf_docs_data.extend(unselected_combination_product_template)
        print(f'{len(self.pdf_docs_data)=}')
        return self.pdf_docs_data

    def get_unselected_combination_product_template(self):
        """
        Наполняет шаблон с невыбранным средством PDF
        с учётом категории
        """
        products = []
        for key, data in self.rus_selection_result.items():
            if key.startswith('product_'):
                product_name = data['Название средства']

                unselected_combination_product_data = get_base_info_by_product(
                    info_data=self.info_data,
                    product_name=product_name,
                )

                template_data = {
                    # исходное средство
                    'Вывод': data['Вывод'],
                    'Путь к изображению бренд-линии': Path("00_base/source/imagine_border/border_fiolet.jpg"),
                    'Путь для сохранения pdf-файла': format_product_filename(
                        product_title=product_name,
                        path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                    ),
                }

                template_data.update(PDF_STRUCTURE['Невыбранное средство'])
                template_data.update(unselected_combination_product_data)
                products.append(template_data)

        return products

    def get_best_combination_product_template(self):
        """
        Наполняет шаблон с лучшим средством PDF
        с учётом категории
        """
        data = self.rus_selection_result['Подобранное средство']
        product_name = data['Название средства']

        best_combination_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
        )

        template_data = {
            # исходное средство
            'Вывод': data['Вывод'],
            'Путь к изображению бренд-линии': Path("00_base/source/imagine_border/border_green.jpg"),
            'Путь для сохранения pdf-файла': format_product_filename(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
            ),
        }

        template_data.update(PDF_STRUCTURE['Подобранное средство'])
        template_data.update(best_combination_product_data)

        return template_data

    def get_source_product_template(self) -> dict:
        """
        Наполняет шаблон PDF для исходного средства
        :return: словарь с информацией для создания PDF-документа
        """

        data = self.rus_selection_result['Исходное средство']
        source_product_name = data['Название средства']

        base_source_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=source_product_name,
        )

        template_data = {
            # исходное средство
            'Плюсы': data['Плюсы'],
            'Минусы': data['Минусы'],
            'Путь к изображению бренд-линии': Path("00_base/source/imagine_border/border_green.jpg"),
            'Путь для сохранения pdf-файла': format_product_filename(
                product_title=source_product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
            ),
        }

        template_data.update(PDF_STRUCTURE['Исходное средство'])
        template_data.update(base_source_product_data)

        return template_data
