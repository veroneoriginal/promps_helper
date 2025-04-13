# pylint: disable=C0301:: line-too-long
# pylint: disable=E0611: no-name-in-module
"""
Создание PDF-документов для задачи 'Разбор состава одного средства'
"""
from pathlib import Path

from pdf.pdf_data_processing.tasks_logic.base_task import get_base_info_by_product
from pdf.pdf_data_processing.tasks_utils import get_path_for_save_pdf, calculate_price_per_standard_unit
from source.structure_folders import GREEN_VERTICAL_BRAND_LINE_PATH

ADDITIONAL_ELEMENTS_BY_PRODUCT_CATEGORY = {
    "Уход за кожей лица": [
        ('Paragraph', {'Текст': '<b>Влияние на тип кожи:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Влияние на тип кожи', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень SPF:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Уровень SPF', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Время нанесения:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Время нанесения', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень pH:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Уровень pH', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Интенсивность пилинга:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Интенсивность пилинга', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Эффект на область глаз:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Эффект на область глаз', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Уход за телом': [
        ('Paragraph', {'Текст': '<b>Влияние на тип кожи:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Влияние на тип кожи', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Интенсивность пилинга:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Интенсивность пилинга', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Длительность защиты:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Длительность защиты', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Пенообразование:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Пенообразование', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Макияж': [
        ('Paragraph', {'Текст': '<b>Стойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Стойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Финиш:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Финиш', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Пигментация:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Пигментация', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Покрытие:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Покрытие', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Водостойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Водостойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень SPF:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Уровень SPF', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Парфюмерия': [
        ('Paragraph', {'Текст': '<b>Основные ноты:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Основные ноты', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Стойкость:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Стойкость', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Раскрытие аромата:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Раскрытие аромата', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Стайлинг волос': [
        ('Paragraph', {'Текст': '<b>Степень фиксации:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Степень фиксации', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Ощущение на волосах:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Ощущение на волосах', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Уход за зубами и полостью рта': [
        ('Paragraph', {'Текст': '<b>Отбеливающий эффект:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Отбеливающий эффект', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Уровень чувствительности:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Уровень чувствительности', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Длительность свежести дыхания:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Длительность свежести дыхания', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Абразивность:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Абразивность', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Содержание фтора:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Содержание фтора', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Антибактериальный эффект:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Антибактериальный эффект', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Без содержания спирта:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Без содержания спирта', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Время полоскания:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Время полоскания', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Тип вкуса/аромата:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Тип вкуса/аромата', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Ощущение жжения:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Ощущение жжения', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Уход за губами': [
        ('Paragraph', {'Текст': '<b>Увлажняющий эффект:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Увлажняющий эффект', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Наличие SPF:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Наличие SPF', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Восстанавливающий эффект:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Восстанавливающий эффект', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Тип финиша:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Тип финиша', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Аромат или вкус:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Аромат или вкус', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Наличие оттенка:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Наличие оттенка', 'Стиль': 'ACOP_normal_3'}),
    ],
    'Стирка и уход за бельём': [
        ('Paragraph', {'Текст': '<b>Степень смягчения ткани:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Степень смягчения ткани', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Тип аромата:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Тип аромата', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Интенсивность аромата:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Интенсивность аромата', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Снижение статического эффекта:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Снижение статического эффекта', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Эффект лёгкой глажки:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Эффект лёгкой глажки', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Подходит для детской одежды:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Подходит для детской одежды', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Концентрированный кондиционер:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Концентрированный кондиционер', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Биоразлагаемая формула:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Биоразлагаемая формула', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Типы тканей:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Типы тканей', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Температурный режим:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Температурный режим', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Удаление пятен:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Удаление пятен', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Защита цвета:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Защита цвета', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Для белого белья:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Для белого белья', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Гипоаллергенность:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Гипоаллергенность', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Удаление остатков моющего средства:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Удаление остатков моющего средства', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Нужно ли дополнительное полоскание:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Нужно ли дополнительное полоскание', 'Стиль': 'ACOP_normal_3'}),
        ('Paragraph', {'Текст': '<b>Дополнительная свежесть ткани:</b>', 'Стиль': 'ACOP_bold_1'}),
        ('Spacer', {'width': 1, 'height': 13}),
        ('Paragraph', {'Ключ в подборке': 'Дополнительная свежесть ткани', 'Стиль': 'ACOP_normal_3'}),
    ],
}

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
            ('Paragraph', {'Текст': '<b>Разбор состава</b>', 'Стиль': 'ACOP_title_2'}),
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
            ('Paragraph', {'Текст': '<b>Основные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Основные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Активные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Активные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph',
             {'Текст': '<b>Увлажняющие и ухаживающие компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph',
             {'Ключ в подборке': 'Увлажняющие и ухаживающие компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Консерванты и регуляторы pH:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Консерванты и регуляторы pH', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Дополнительные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph',
             {'Ключ в подборке': 'Дополнительные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph',
             {'Текст': '<b>Запрещенные или нежелательные компоненты:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph',
             {'Ключ в подборке': 'Запрещенные или нежелательные компоненты', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph',
             {'Ключ в подборке': 'Плюсы', 'Стиль': 'ACOP_normal_3'}),
            ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'ACOP_normal_3'}),
            # Сюда вставим дополнительную информацию по категории индекс -4
            ('Paragraph', {'Текст': '<b>Вывод:</b>', 'Стиль': 'ACOP_bold_1'}),
            ('Spacer', {'width': 1, 'height': 13}),
            ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'ACOP_normal_3'}),
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

        template = self.get_base_template(one_product_data=self.rus_selection_result)
        self.pdf_docs_data.append(template)

        return self.pdf_docs_data

    def get_additional_product_data_by_category(
            self,
            category_name: str,
            one_product_data: dict,
    ) -> dict | None:
        """
        Возвращает дополнительную информацию в зависимости от
        категории подборки ("Стайлинг волос", "Макияж" и т.д.)
        :param category_name: категория подборки
        :param one_product_data: данные одного средства из ответа нейронки
        :return: dict
        """

        CATEGORY_WITH_ADDITIONAL_DATA = {
            "Уход за кожей лица": self._category_facial_skin_care,
            "Уход за телом": self._category_body_care,
            "Макияж": self._category_makeup,
            "Парфюмерия": self._category_perfumery,
            "Стайлинг волос": self._category_hair_styling,
            "Уход за зубами и полостью рта": self._category_oral_care,
            "Уход за губами": self._category_lip_care,
            "Стирка и уход за бельём": self._category_laundry_care,
        }

        additional_data_func = CATEGORY_WITH_ADDITIONAL_DATA.get(
            category_name, None
        )

        if additional_data_func:
            return additional_data_func(one_product_data=one_product_data)
        return None

    def get_base_template(
            self,
            one_product_data: dict,
    ) -> dict:
        """
        Наполняет базовый шаблон PDF
        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с информацией для создания PDF-документа
        """

        product_name = self.rus_selection_result['Название средства']
        product_name_lower = product_name.lower().strip()
        product_article = one_product_data['Артикул в Золотом Яблоке']

        product_data_in_data_tools = self.info_data['Средства'][product_name_lower][product_article]

        template_data = {  # отличается:
            'Плюсы': one_product_data['Плюсы'],
            'Минусы': one_product_data['Минусы'],
            'Текстура': one_product_data['Текстура'],
            'Соотношение цены': calculate_price_per_standard_unit(
                quantity=product_data_in_data_tools['Количество меры (число)'],
                unit=product_data_in_data_tools['Юниты меры (мл/шт)'],
                price_rub=product_data_in_data_tools['Стоимость руб'],
            ),
            'Путь к изображению бренд-линии': GREEN_VERTICAL_BRAND_LINE_PATH,
            'Путь для сохранения pdf-файла': Path(get_path_for_save_pdf(
                product_title=product_name,
                path_to_output_folder_pdf_file=self.path_to_output_folder_pdf_file,
                product_article=product_article,
            )
            ),
            'Основные компоненты': one_product_data['Основные компоненты'],
            'Активные компоненты': one_product_data['Активные компоненты'],
            'Увлажняющие и ухаживающие компоненты': one_product_data['Увлажняющие и ухаживающие компоненты'],
            'Консерванты и регуляторы pH': one_product_data['Консерванты и регуляторы pH'],
            'Дополнительные компоненты': one_product_data['Дополнительные компоненты'],
            'Запрещенные или нежелательные компоненты': one_product_data[
                'Запрещенные или нежелательные компоненты'],
            'Вывод': one_product_data['Вывод'],
        }

        base_product_data = get_base_info_by_product(
            info_data=self.info_data,
            product_name=product_name,
            product_article=product_article,
        )

        template_data.update(base_product_data)
        template_data.update(PDF_STRUCTURE['Базовая категория'])

        # Добавляем дополнительные данные по категории
        additional_data = self.get_additional_product_data_by_category(
            category_name=self.collection_data['Категория'],
            one_product_data=one_product_data,
        )
        if additional_data:
            template_data.update(additional_data)
            # Добавляем в структуру шаблона дополнительные блоки
            # в зависимости от категории продукта
            additional_block = ADDITIONAL_ELEMENTS_BY_PRODUCT_CATEGORY[
                self.collection_data['Категория']
            ]

            template_data['Элементы и стили'][-3:-3] = additional_block

        return template_data

    def _category_hair_styling(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Стайлинг волос"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            'Степень фиксации': one_product_data['Степень фиксации'],
            'Ощущение на волосах': one_product_data['Ощущение на волосах'],
        }

    def _category_makeup(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Макияж"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            'Стойкость': one_product_data['Стойкость'],
            'Финиш': one_product_data['Финиш'],
            'Пигментация': one_product_data['Пигментация'],
            'Покрытие': one_product_data['Покрытие'],
            'Водостойкость': one_product_data['Водостойкость'],
            'Уровень SPF': one_product_data['Уровень SPF'],
        }

    def _category_body_care(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за телом"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            'Влияние на тип кожи': one_product_data['Влияние на тип кожи'],
            'Интенсивность пилинга': one_product_data['Интенсивность пилинга'],
            'Длительность защиты': one_product_data['Длительность защиты'],
            'Пенообразование': one_product_data['Пенообразование'],
        }

    def _category_facial_skin_care(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за кожей лица"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            'Влияние на тип кожи': one_product_data['Влияние на тип кожи'],
            'Уровень SPF': one_product_data['Уровень SPF'],
            'Время нанесения': one_product_data['Время нанесения'],
            'Уровень pH': one_product_data['Уровень pH'],
            'Интенсивность пилинга': one_product_data['Интенсивность пилинга'],
            'Эффект на область глаз': one_product_data['Эффект на область глаз'],
        }

    def _category_perfumery(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Парфюмерия"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            'Основные ноты': one_product_data['Основные ноты'],
            'Стойкость': one_product_data['Стойкость'],
            'Раскрытие аромата': one_product_data['Раскрытие аромата'],
        }

    def _category_oral_care(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за зубами и полостью рта"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            "Отбеливающий эффект": one_product_data["Отбеливающий эффект"],
            "Уровень чувствительности": one_product_data["Уровень чувствительности"],
            "Длительность свежести дыхания": one_product_data["Длительность свежести дыхания"],
            "Абразивность": one_product_data["Абразивность"],
            "Содержание фтора": one_product_data["Содержание фтора"],
            "Антибактериальный эффект": one_product_data["Антибактериальный эффект"],
            "Без содержания спирта": one_product_data["Без содержания спирта"],
            "Время полоскания": one_product_data["Время полоскания"],
            "Тип вкуса/аромата": one_product_data["Тип вкуса/аромата"],
            "Ощущение жжения": one_product_data["Ощущение жжения"],

        }

    def _category_lip_care(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Уход за губами"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            "Увлажняющий эффект": one_product_data["Увлажняющий эффект"],
            "Наличие SPF": one_product_data["Наличие SPF"],
            "Восстанавливающий эффект": one_product_data["Восстанавливающий эффект"],
            "Тип финиша": one_product_data["Тип финиша"],
            "Аромат или вкус": one_product_data["Аромат или вкус"],
            "Наличие оттенка": one_product_data["Наличие оттенка"],
        }

    def _category_laundry_care(self, one_product_data: dict) -> dict:
        """
        Задача "Разбор состава одного средства"
        дополнительные данные для категории "Стирка и уход за бельём"

        :param one_product_data: данные одного средства из ответа нейронки
        :return: словарь с специфичными данными
        """

        return {
            "Степень смягчения ткани": one_product_data["Степень смягчения ткани"],
            "Тип аромата": one_product_data["Тип аромата"],
            "Интенсивность аромата": one_product_data["Интенсивность аромата"],
            "Снижение статического эффекта": one_product_data["Снижение статического эффекта"],
            "Эффект лёгкой глажки": one_product_data["Эффект лёгкой глажки"],
            "Подходит для детской одежды": one_product_data["Подходит для детской одежды"],
            "Концентрированный кондиционер": one_product_data["Концентрированный кондиционер"],
            "Биоразлагаемая формула": one_product_data["Биоразлагаемая формула"],
            "Типы тканей": one_product_data["Типы тканей"],
            "Температурный режим": one_product_data["Температурный режим"],
            "Удаление пятен": one_product_data["Удаление пятен"],
            "Защита цвета": one_product_data["Защита цвета"],
            "Для белого белья": one_product_data["Для белого белья"],
            "Гипоаллергенность": one_product_data["Гипоаллергенность"],
            "Удаление остатков моющего средства": one_product_data["Удаление остатков моющего средства"],
            "Нужно ли дополнительное полоскание": one_product_data["Нужно ли дополнительное полоскание"],
            "Дополнительная свежесть ткани": one_product_data["Дополнительная свежесть ткани"],
        }
