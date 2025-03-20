# pylint: skip-file
""" Настройки для формирования PDF-документов по подборкам по задачам """


def calc_framesize(document_size: tuple) -> tuple:
    """
    Для расчёта размеров фрейма в поинтах
    """
    return document_size[0] * 0.75, document_size[1] * 0.75


# print(calc_framesize(document_size=(1024-80, 1280)))

def get_pdf_structure(
        task: str,
        category: str,
) -> dict:
    """
    Возвращает структуру PDF-документа в зависимости от
    задачи и категории

    :param task: код задачи
    :param category: категория подборки
    :return: структуру PDF-документа
    """

    category_items = PDF_SETTINGS[task]
    return category_items.get(category) or category_items.get('Базовая категория')


PDF_SETTINGS = {
    'Лучшее средство': {
        'Базовая категория':
            {
                'Пути бренд-линий': {
                    'Цвет_1': "00_base/source/imagine_border/border_green.jpg",
                    'Цвет_2': "00_base/source/imagine_border/border_fiolet.jpg",
                },
                'Размеры бренд-линии': (80, 1280),
                'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
                'Элементы и стили': [
                    ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
                    ('Spacer', {'width': 1, 'height': 25}),
                    ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BP_normal_2', 'Заглавными': True}),
                    ('Spacer', {'width': 1, 'height': 20}),
                    ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BP_title_1'}),
                    ('Spacer', {'width': 1, 'height': 20}),
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
    },
    'Разбор состава одного средства':
        {
            'Базовая категория':
                {
                    'Пути бренд-линий': {
                        'Цвет_1': "00_base/source/imagine_border/border_green.jpg",
                        'Цвет_2': "00_base/source/imagine_border/border_fiolet.jpg",
                    },
                    'Размеры бренд-линии': (80, 1280),
                    'Размеры документа': (1024, 1280),  # (ширина, высота) в пикселях
                    'Элементы и стили': [
                        ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
                        ('Spacer', {'width': 1, 'height': 25}),
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
                        ('Paragraph',
                         {'Текст': '<b>Минусы:</b>', 'Стиль': 'ACOP_bold_1'}),
                        ('Spacer', {'width': 1, 'height': 10}),
                        ('Paragraph',
                         {'Ключ в подборке': 'Минусы', 'Стиль': 'ACOP_normal_3'}),
                        ('Paragraph', {'Текст': '<b>Вывод:</b>', 'Стиль': 'ACOP_bold_1'}),
                        ('Spacer', {'width': 1, 'height': 10}),
                        ('Paragraph',
                         {'Ключ в подборке': 'Вывод', 'Стиль': 'ACOP_normal_3'}),
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
            'Макияж':
                {...}
        }
}

# ТУТ ОСТАНОВИЛСЯ
