# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Лучая пара'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import (
    get_path_for_save_pdf,
)

PDF_STRUCTURE = {
    'Лучшая пара': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (1281, 85),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1280, 1024),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Spacer', {'width': 1, 'height': 11}),
            ('Image', {'Ключ в подборке': 'Путь к изображению средства 1', 'width': 640, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Image', {'Ключ в подборке': 'Путь к изображению средства 2', 'width': 640, 'height': 1280}),
            # ('FreeText', {'Текст': '&', 'x': 280, 'y': 426,
            #               'font_name': 'Montserrat-Bold',
            #               'font_size': 70, 'font_color': "#BBE02CFF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображений: https://goldapple.ru/', 'x': 20, 'y': 866,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('FrameBreak', {}),
            # описание средства 1
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 1', 'Стиль': 'BEST_COUPLE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 1', 'Стиль': 'BEST_COUPLE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 1', 'Стиль': 'BEST_COUPLE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 1', 'Стиль': 'BEST_COUPLE_base_price'}),
            ('FrameBreak', {}),
            # описание средства 2
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 2', 'Стиль': 'BEST_COUPLE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 2', 'Стиль': 'BEST_COUPLE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 2', 'Стиль': 'BEST_COUPLE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 2', 'Стиль': 'BEST_COUPLE_base_price'}),
            ('FreeImage',
             {
                 'Ключ в подборке': 'Путь к изображению галочки',
                 'x': -170,
                 'y': 180,
                 'width': 225,
                 'height': 225,
                 'preserve_aspect_ratio': True,
             }
             ),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (0, 85), (633, 940)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (1, (680, 554), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (2, (680, 106), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
    'Не лучшая пара': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (1281, 85),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1280, 1024),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Spacer', {'width': 1, 'height': 11}),
            ('Image', {'Ключ в подборке': 'Путь к изображению средства 1', 'width': 640, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Image', {'Ключ в подборке': 'Путь к изображению средства 2', 'width': 640, 'height': 1280}),
            # ('FreeText', {'Текст': '&', 'x': 280, 'y': 426,
            #               'font_name': 'Montserrat-Bold',
            #               'font_size': 70, 'font_color': "#BBE02CFF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображений: https://goldapple.ru/', 'x': 20, 'y': 866,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('FrameBreak', {}),
            # описание средства 1
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 1', 'Стиль': 'BEST_COUPLE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 1', 'Стиль': 'BEST_COUPLE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 1', 'Стиль': 'BEST_COUPLE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 1', 'Стиль': 'BEST_COUPLE_base_price'}),
            ('FrameBreak', {}),
            # описание средства 2
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 2', 'Стиль': 'BEST_COUPLE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 2', 'Стиль': 'BEST_COUPLE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 2', 'Стиль': 'BEST_COUPLE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 2', 'Стиль': 'BEST_COUPLE_base_price'}),
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (0, 85), (633, 940)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (1, (680, 554), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (2, (680, 106), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
}


class BestCouplePDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Лучшая пара"
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
        Задача "Лучшая пара"
        :return: Возвращает список с данными для создания документов
        """

        for key, value in self.rus_selection_result.items():
            if key.startswith('set_'):
                if value['Лучший набор']:
                    template = self.get_best_set_template(all_data=value)
                else:
                    template = self.get_no_best_set_template(all_data=value)
                self.pdf_docs_data.append(template)
        return self.pdf_docs_data

    def get_couple_products_data(
            self,
            all_data: dict,
    ) -> dict:
        """
        Возвращает данные по паре средств
        :param all_data: данные со всеми средствами
        """
        product_1_data = all_data['product_1']
        product_1_name = product_1_data['Название средства']
        product_1_article = product_1_data['Артикул в Золотом Яблоке']

        product_1_base_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_1_name,
            product_article=product_1_article,
        )

        product_2_data = all_data['product_2']
        product_2_name = product_2_data['Название средства']
        product_2_article = product_2_data['Артикул в Золотом Яблоке']

        product_2_base_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_2_name,
            product_article=product_2_article,
        )

        template_data = {
            'Путь к изображению средства 1': product_1_base_data['Путь к изображению средства'],
            'Название средства 1': product_1_name,
            'Тип продукта 1': product_1_base_data['Тип продукта'],
            'Артикул 1': f'{product_1_base_data["Артикул"]}',
            'Количество мера / цена 1': product_1_base_data['Количество мера / цена'],

            'Путь к изображению средства 2': product_2_base_data['Путь к изображению средства'],
            'Название средства 2': product_2_name,
            'Тип продукта 2': product_2_base_data['Тип продукта'],
            'Артикул 2': f'{product_2_base_data["Артикул"]}',
            'Количество мера / цена 2': product_2_base_data['Количество мера / цена'],
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_1_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_1_article,
            ),
        }

        return template_data

    def get_best_set_template(
            self,
            all_data: dict,
    ) -> dict:
        """
        Наполняет шаблон с лучшей парой средств
        :param all_data: данные со всеми средствами
        :return: список с шаблонами
        """
        template_data = self.get_couple_products_data(all_data=all_data)
        template_data['Путь к изображению галочки'] = Path('00_base/source/check/v2.png')
        template_data['Путь к изображению бренд-линии'] = Path('00_base/source/imagine_border/border_green_horizontal.jpg')
        template_data.update(PDF_STRUCTURE['Лучшая пара'])

        return template_data

    def get_no_best_set_template(
            self,
            all_data: dict
    ) -> dict:
        """
        Наполняет шаблон с не лучшим набором.
        :param all_data: данные со всеми средствами
        :return: список с шаблонами
        """
        template_data = self.get_couple_products_data(all_data=all_data)
        template_data.update(PDF_STRUCTURE['Не лучшая пара'])
        template_data['Путь к изображению бренд-линии'] = Path(
            '00_base/source/imagine_border/border_fiolet_horizontal.jpg')

        return template_data
