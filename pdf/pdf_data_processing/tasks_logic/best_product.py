# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Лучшее средство'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import get_path_for_save_pdf

PDF_STRUCTURE = {
    'Базовая категория':
        {
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
                ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BP_normal_2', 'Заглавными': True}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BP_title_1'}),
                ('Spacer', {'width': 1, 'height': 30}),
                ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BP_base_price_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BP_bold_1'}),
                ('Spacer', {'width': 1, 'height': 15}),
                ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BP_normal_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BP_bold_1'}),
                ('Spacer', {'width': 1, 'height': 15}),
                ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BP_normal_1'}),
            ],
            'Шаблоны страниц с фреймами': {
                'template_1':
                    (
                        (0, (100, 0), (596, 966)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    )
            },
        },
}


class BestProductPDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Лучшее средство"
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
        Задача "Лучшее средство"
        :return: Возвращает список с данными для создания документов
        """

        for key, value in self.rus_selection_result.items():
            if key.startswith('product_'):
                template = self.get_base_template(one_product_data=value)
                self.pdf_docs_data.append(template)

        return self.pdf_docs_data

    def get_base_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет базовый шаблон PDF
        :param one_product_data: данные одного средства
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = one_product_data['Название средства']
        product_article = one_product_data['Артикул в Золотом Яблоке']

        template_data = {  # отличается:
            'Плюсы': one_product_data['Плюсы'],
            'Минусы': one_product_data['Минусы'],
            'Путь к изображению бренд-линии': Path(self.get_brand_line_path(
                value=one_product_data['Лучшее средство'],
            )
            ),

            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            ),
        }

        base_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data.update(base_product_data)
        template_data.update(PDF_STRUCTURE['Базовая категория'])

        return template_data

    def get_brand_line_path(
            self,
            value: bool
    ):
        """
        Возвращает путь к файлу с нужной бренд-линией для нанесения на PDF
        :param value: True или False (лучшее/не лучшее)
        :return: путь до файла с бренд-линией
        """

        BRAND_LINE_PATH = {
            'Цвет_1': "00_base/source/imagine_border/border_green.jpg",
            'Цвет_2': "00_base/source/imagine_border/border_fiolet.jpg",
        }

        return BRAND_LINE_PATH['Цвет_1'] if value else BRAND_LINE_PATH['Цвет_2']
