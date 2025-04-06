# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Лучшее средство без канцерогенов'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import get_path_for_save_pdf

PDF_STRUCTURE = {
    'Лучшее средство':
        {
            'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
            'Размеры бренд-линии': (85, 1280),
            'Координаты вставки бренд-линии': [(0, 0), ],
            'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
            'Элементы и стили': [
                ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
                ('Spacer', {'width': 1, 'height': 34}),
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
                ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BPWC_normal_2', 'Заглавными': True}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BPWC_title_1'}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BPWC_base_price_1'}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BPWC_normal_1'}),
                ('Spacer', {'width': 1, 'height': 13}),
                ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BPWC_normal_1'}),
                ('Spacer', {'width': 1, 'height': 13}),
                ('Paragraph', {'Текст': '<b>Канцерогены:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Канцерогены', 'Стиль': 'BPWC_normal_1'}),
            ],
            'Шаблоны страниц с фреймами': {
                'template_1':
                    (
                        (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    )
            },

        },
    'Не лучшее средство':
        {
            'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
            'Размеры бренд-линии': (85, 1280),
            'Координаты вставки бренд-линии': [(0, 0), ],
            'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
            'Элементы и стили': [
                ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
                ('Spacer', {'width': 1, 'height': 34}),
                ('FreeText',
                 {'Ключ в подборке': 'Артикул', 'x': 0, 'y': 666,
                  'font_name': 'Montserrat-Regular',
                  'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
                ('FreeText',
                 {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': 0, 'y': 54,
                  'font_name': 'Montserrat-Regular',
                  'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
                ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BPWC_normal_2', 'Заглавными': True}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BPWC_title_1'}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BPWC_base_price_1'}),
                ('Spacer', {'width': 1, 'height': 26}),
                ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BPWC_normal_1'}),
                ('Spacer', {'width': 1, 'height': 13}),
                ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BPWC_normal_1'}),
                ('Spacer', {'width': 1, 'height': 13}),
                ('Paragraph', {'Текст': '<b>Канцерогены:</b>', 'Стиль': 'BPWC_bold_1'}),
                ('Spacer', {'width': 1, 'height': 20}),
                ('Paragraph', {'Ключ в подборке': 'Канцерогены', 'Стиль': 'BPWC_normal_1'}),
            ],
            'Шаблоны страниц с фреймами': {
                'template_1':
                    (
                        (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    )
            },

        },
}


class BestProductWithOutConcerogensPDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Лучшее средство без канцерогенов"
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
                template = self.get_template(one_product_data=value)
                self.pdf_docs_data.append(template)

        return self.pdf_docs_data

    def get_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет шаблон PDF лучшего или не лучшего средства
        :param one_product_data: данные одного средства
        :return: словарь с информацией для создания PDF-документа
        """

        if one_product_data['Лучшее средство']:
            template = self.get_best_product_template(
                one_product_data=one_product_data,
            )
        else:
            template = self.get_no_best_product_template(
                one_product_data=one_product_data,
            )
        return template

    def get_base_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет базовый шаблон PDF
        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = one_product_data['Название средства']
        product_article = one_product_data['Артикул в Золотом Яблоке']

        cancirogens = one_product_data['Канцерогены']
        template_data = {
            'Плюсы': one_product_data['Плюсы'],
            'Минусы': one_product_data['Минусы'],
            'Путь для сохранения pdf-файла': get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            ),
            'Канцерогены': cancirogens if cancirogens else "Нет",
        }

        base_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data.update(base_product_data)

        return template_data

    def get_best_product_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Возвращает шаблон PDF для лучшего средства
        :param one_product_data: данные одного средства
        :return: словарь с информацией для создания PDF-документа
        """

        template = self.get_base_template(one_product_data=one_product_data)
        template['Путь к изображению галочки'] = Path("00_base/source/check/v2.png")
        template['Путь к изображению бренд-линии'] = Path('00_base/source/imagine_border/border_green.jpg')
        template.update(PDF_STRUCTURE['Лучшее средство'])

        return template

    def get_no_best_product_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Возвращает шаблон PDF для не лучшего средства
        :param one_product_data: данные одного средства
        :return: словарь с информацией для создания PDF-документа
        """

        template = self.get_base_template(one_product_data=one_product_data)
        template['Путь к изображению бренд-линии'] = Path('00_base/source/imagine_border/border_fiolet.jpg')
        template.update(PDF_STRUCTURE['Не лучшее средство'])

        return template
