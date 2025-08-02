# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Аналог'
"""
from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import (
    get_path_for_save_pdf,
)
from source.structure_folders import ORANGE_LIGHT_VERTICAL_BRAND_LINE_PATH

PDF_STRUCTURE = {
    'Исходный шаблон': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1024),
        'Координаты вставки бренд-линии': [(0, 0), (1955, 0)],
        'Размеры документа': (2040, 1024),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства 1', 'width': 728, 'height': 1280}),
            ('FreeText',
             {'Текст': 'Правообладатель изображений: https://goldapple.ru/', 'x': 85, 'y': 460,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('FreeRect', {'x': 0, 'y': -510,
                          'width': 716,
                          'height': 70, 'fill_color': "#F2F2F2"}),

            ('Image', {'Ключ в подборке': 'Путь к изображению средства 2', 'width': 728, 'height': 1280}),
            # ('FreeText', {'Текст': '&', 'x': 320, 'y': 475,
            #               'font_name': 'Montserrat-Bold',
            #               'font_size': 80, 'font_color': "#BBE02CFF", 'bold': False, 'align': 'left'}),

            ('FrameBreak', {}),
            # описание средства 1
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 1', 'Стиль': 'ANALOGUE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 1', 'Стиль': 'ANALOGUE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 1', 'Стиль': 'ANALOGUE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 1', 'Стиль': 'ANALOGUE_base_price'}),
            ('FrameBreak', {}),
            # описание средства 2
            ('Spacer', {'width': 1, 'height': 106}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта 2', 'Стиль': 'ANALOGUE_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Название средства 2', 'Стиль': 'ANALOGUE_title_1'}),
            ('Paragraph', {'Ключ в подборке': 'Артикул 2', 'Стиль': 'ANALOGUE_normal_1'}),
            ('Spacer', {'width': 1, 'height': 11}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена 2', 'Стиль': 'ANALOGUE_base_price'}),
            ('FrameBreak', {}),
            # выводы
            ('FreeRect', {'x': -20, 'y': -1024,
                          'width': 700,
                          'height': 1100, 'fill_color': "#F2F2F2"}),
            ('Paragraph', {'Ключ в подборке': 'Вывод коротко', 'Стиль': 'ANALOGUE_text'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Сходства</b>', 'Стиль': 'ANALOGUE_text_title'}),
            ('Paragraph', {'Ключ в подборке': 'Сходства', 'Стиль': 'ANALOGUE_text'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Различия</b>', 'Стиль': 'ANALOGUE_text_title'}),
            ('Paragraph', {'Ключ в подборке': 'Различия', 'Стиль': 'ANALOGUE_text'}),
            ('Spacer', {'width': 1, 'height': 20}),
            ('Paragraph', {'Текст': '<b>Вывод</b>', 'Стиль': 'ANALOGUE_text_title'}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'ANALOGUE_text'}),
            ('Spacer', {'width': 1, 'height': 20}),

        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (0, 0), (720, 1032)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (1, (742, 530), (540, 480)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (2, (742, 10), (540, 480)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (2, (1300, 10), (640, 970)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
        },
    },
}


class AnaloguePDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Аналог"
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

        template = self.get_analogue_template(all_data=self.rus_selection_result)
        self.pdf_docs_data.append(template)
        return self.pdf_docs_data

    def get_analogue_products_data(
            self,
            all_data: dict,
    ) -> dict:
        """
        Возвращает данные по паре средств
        :param all_data: данные со всеми средствами
        """
        product_1_data = all_data['source_product']
        product_1_name = product_1_data['Название средства']
        product_1_article = product_1_data['Артикул в Золотом Яблоке']

        product_1_base_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_1_name,
            product_article=product_1_article,
        )

        product_2_data = all_data['analog_product']
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
            'Артикул 1': product_1_base_data["Артикул"],
            'Количество мера / цена 1': product_1_base_data['Количество мера / цена'],

            'Путь к изображению средства 2': product_2_base_data['Путь к изображению средства'],
            'Название средства 2': product_2_name,
            'Тип продукта 2': product_2_base_data['Тип продукта'],
            'Артикул 2': product_2_base_data["Артикул"],
            'Количество мера / цена 2': product_2_base_data['Количество мера / цена'],

            'Путь к изображению бренд-линии': ORANGE_LIGHT_VERTICAL_BRAND_LINE_PATH,
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_1_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_1_article,
            ),
        }

        return template_data

    def get_analogue_template(
            self,
            all_data: dict,
    ) -> dict:
        """
        Наполняет шаблон с лучшей парой средств
        :param all_data: данные со всеми средствами
        :return: список с шаблонами
        """
        template_data = self.get_analogue_products_data(all_data=all_data)
        info_data = {
            'Вывод': all_data['Вывод'],
            'Вывод коротко': all_data['Вывод коротко'],
            'Сходства': all_data['Сходства'],
            'Различия': all_data['Различия'],
        }
        template_data.update(info_data)

        template_data.update(PDF_STRUCTURE['Исходный шаблон'])
        return template_data
