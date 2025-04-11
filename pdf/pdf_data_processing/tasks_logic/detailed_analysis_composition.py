# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Подробный анализ состава'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import get_path_for_save_pdf, calculate_price_per_standard_unit

PDF_STRUCTURE = {
    'Базовая категория': {
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
        'Элементы и стили': [
            ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
            ('Spacer', {'width': 1, 'height': 34}),
            ('FreeText',
             {'Ключ в подборке': 'Артикул', 'x': 600, 'y': 666,
              'font_name': 'Montserrat-Regular',
              'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
            ('FreeText',
             {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -40, 'y': 54,
              'font_name': 'Montserrat-Regular',
              'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
            ('Paragraph', {'Текст': '<b>Подробный разбор состава</b>', 'Стиль': 'ACOP_title_2'}),
            ('Spacer', {'width': 1, 'height': 40}),
            ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'ACOP_normal_2'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'ACOP_title_1'}),
            ('Spacer', {'width': 1, 'height': 26}),
            ('Paragraph', {'Текст': '<b>Цена за средство:</b>', 'Стиль': 'ACOP_bold_2'}),
            ('Spacer', {'width': 1, 'height': 34}),
            ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'ACOP_base_price_1'}),
            ('Spacer', {'width': 1, 'height': 54}),
            ('Paragraph', {'Текст': '<b>Соотношение цены:</b>', 'Стиль': 'ACOP_bold_2'}),
            ('Spacer', {'width': 1, 'height': 34}),
            ('Paragraph', {'Ключ в подборке': 'Соотношение цены', 'Стиль': 'ACOP_price_ratio_1'}),

            ('NextPageTemplate', {'template_id': 'template_2'}),
            ('PageBreak', {}),
            # следующая страница
        ],
        'Шаблоны страниц с фреймами': {
            'template_1':
                (
                    (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                ),
            'template_2':
                (
                    (0, (133, 85), (794, 1094)),
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                )

        },

    },

}


class DetailedAnalysisCompositionPDFTemplateCreator:
    """
    Готовит данные для PDF-документов по задаче "Подробный анализ состава"
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
        Задача "Подробный анализ состава"
        :return: Возвращает список с данными для создания документов
        """

        template = self.get_base_template(one_product_data=self.rus_selection_result)
        self.pdf_docs_data.append(template)

        return self.pdf_docs_data

    def get_base_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет базовый шаблон PDF
        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = one_product_data['Исходное средство']['Название средства']
        product_name_lower = product_name.lower().strip()

        product_article = one_product_data['Исходное средство']['Артикул в Золотом Яблоке']

        product_data_in_data_tools = self.info_data['Средства'][product_name_lower][product_article]

        template_data = {  # отличается:
            'Соотношение цены': calculate_price_per_standard_unit(
                quantity=product_data_in_data_tools['Количество меры (число)'],
                unit=product_data_in_data_tools['Юниты меры (мл/шт)'],
                price_rub=product_data_in_data_tools['Стоимость руб'],
            ),
            'Путь к изображению бренд-линии': Path("00_base/source/imagine_border/border_orange_light.jpg"),
            'Путь для сохранения pdf-файла': Path(get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            )
            ),

            'Вывод': one_product_data['Вывод'],
        }

        elements_data = self.get_composition_elements_data(
            one_product_data=one_product_data,
        )
        composition_elements_data_for_template = self.get_composition_elements_data_for_template(
            one_product_data=one_product_data,
        )

        base_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data.update(base_product_data)
        template_data.update(elements_data)
        template_data.update(PDF_STRUCTURE['Базовая категория'])
        template_data['Элементы и стили'].extend(composition_elements_data_for_template)

        return template_data

    def get_composition_elements_data_for_template(
            self,
            one_product_data: dict,
    ) -> list:
        """
        Формирует словарь с стилями и абзацами дял вставки в шаблон
        :param one_product_data: данные ответа нейронки
        """
        result_data = []
        for element, _ in one_product_data.items():
            if element.startswith('element_'):
                result_data.extend(
                    self.get_data_template_for_one_element(
                        element_name=element,
                    )
                )
        return result_data

    def get_data_template_for_one_element(
            self,
            element_name: str,
    ) -> list:
        """
        Возвращает список с элементами шаблона и стилями для вставки в документ
        :param element_name: имя элемента из ответа ("element_1", "element_777")
        :return: список с элементами шаблона и стилями для вставки в документ
        """

        return [
            ('Paragraph', {'Ключ в подборке': f'{element_name}_Название элемента', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': f'{element_name}_Для чего элемент', 'Стиль': 'ACOP_normal_3'}),
            ('Spacer', {'width': 1, 'height': -20}),
            ('Paragraph', {'Ключ в подборке': f'{element_name}_Опасность элемента', 'Стиль': 'ACOP_normal_3'}),
            # ('Paragraph', {'Ключ в подборке': f'{element_name}_Чем опасен элемент', 'Стиль': 'ACOP_normal_3'}),
            # ('Paragraph',
            # {'Ключ в подборке': f'{element_name}_Уровень опасности элемента (числом)', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
        ]

    def get_composition_elements_data(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Формирует словарь с данными элементов из состава
        :param one_product_data: данные ответа нейронки
        """
        result_data = {}
        for element, data in one_product_data.items():
            if element.startswith('element_'):
                result_data.update(
                    self.get_one_element_data(
                        element_name=element,
                        one_element_data=data
                    )
                )
        return result_data

    def get_one_element_data(
            self,
            element_name: str,
            one_element_data: dict
    ) -> dict:
        """
        Возвращает словарь с информацией об элементе из состава
        :param element_name: имя элемента из ответа ("element_1", "element_777")
        :param one_element_data: словарь с информацией по элементу
        :return: {'Aqua (Water)': 'Вода используется как растворител ...', ...}
        """
        element_title = one_element_data.get("Название элемента", "Без названия")
        what_is_element_used_for = one_element_data.get("Для чего элемент", "Нет описания")
        is_element_danger = one_element_data.get("Опасен элемент или нет", False)
        element_danger_text = one_element_data.get("Чем опасен элемент", "Нет описания")
        danger_level_smile = self.get_danger_level_smile(is_element_danger=is_element_danger)
        element_danger_text = f'{danger_level_smile} {element_danger_text}'
        element_stop_in_country = one_element_data.get("Элемент запрещён в странах", "").strip()

        is_not_banned = element_stop_in_country.lower() == "не запрещён."
        ban_text = "" if is_not_banned else element_stop_in_country
        what_is_element_used_for_with_ban = [what_is_element_used_for]
        if ban_text:
            what_is_element_used_for_with_ban.append(ban_text)

        return {
            f'{element_name}_Название элемента': element_title,
            f'{element_name}_Для чего элемент': '\n'.join(what_is_element_used_for_with_ban),
            f'{element_name}_Опасность элемента': element_danger_text,
        }

    def get_danger_level_smile(
            self,
            is_element_danger: bool,
    ):
        """
        Возвращает смайлик уровня опасности элемента
        """

        DANGER_SMILES = {
            True: '⚠',
            False: '✅'
        }

        return DANGER_SMILES[is_element_danger]
