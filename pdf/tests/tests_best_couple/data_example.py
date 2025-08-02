# pylint: skip-file

"""
Примеры структур для задачи "Лучшая пара"
"""
from pathlib import Path

TEST_BEST_COUPLE_PATH_PDF_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf'
TEST_BEST_COUPLE_PATH_JPG_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg'
FILE_PATH_TOOLS = '01_test_base/Средства для тестов.xlsx'

TEST_BEST_COUPLE_SELECTION_RESULT = {
    "result": "Набор 2 является лучшим выбором для решения проблем увлажнения и питания волос, а также для частого мытья. Шампунь R+CO Atlantis Moisturizing B5 Shampoo содержит провитамин В5 и экстракт стволовых клеток опунции, которые обеспечивают глубокое увлажнение и поддержание здорового уровня pH, что идеально подходит для сухих волос. Кондиционер R+CO Television Perfect Hair Conditioner дополнительно увлажняет и защищает волосы благодаря маслу бабассу и экстракту ягод можжевельника, не содержит агрессивных компонентов, что делает его подходящим для частого использования. Эти средства в комплексе обеспечивают необходимое увлажнение, питание и защиту волос, не утяжеляя их и поддерживая естественный баланс.",
    "set_1": {
        "result": "Набор 1 содержит шампунь с биотином и провитамином В5, что хорошо для укрепления и увлажнения волос, а также маску с маслами, которые обеспечивают глубокое увлажнение и питание. Однако, маска может быть слишком тяжелой для частого использования, что не соответствует запросу на средства для частого мытья.",
        "best_set": False,
        "product_1": {
            "title": "R+CO Dallas Biotin Thickening Shampoo",
            "article": "24320200017"
        },
        "product_2": {
            "title": "R+CO TELEVISION Perfect Hair Masque",
            "article": "19760310342"
        }
    },
    "set_2": {
        "result": "Набор 2 идеально подходит для увлажнения и питания волос, а также для частого мытья. Шампунь с провитамином В5 и экстрактом стволовых клеток опунции обеспечивает глубокое увлажнение и поддержание здорового уровня pH, а кондиционер с маслом бабассу и экстрактом ягод можжевельника увлажняет и защищает волосы, не утяжеляя их. Отсутствие агрессивных компонентов делает его подходящим для частого использования.",
        "best_set": True,
        "product_1": {
            "title": "R+CO Atlantis Moisturizing B5 Shampoo",
            "article": "24320200015"
        },
        "product_2": {
            "title": "R+CO Television Perfect Hair Conditioner",
            "article": "24320100036"
        }
    }
}

TEST_BEST_COUPLE_COLLECTION_DATA = {
    'Задача': 'Лучшая пара',
    'Категория': 'Шампуни',
}

elem_best_couple = [
    ('Spacer', {'width': 1, 'height': 11}),
    ('Image', {'Ключ в подборке': 'Путь к изображению средства 1', 'width': 640, 'height': 1280}),
    ('Spacer', {'width': 1, 'height': 26}),
    ('Image', {'Ключ в подборке': 'Путь к изображению средства 2', 'width': 640, 'height': 1280}),
    # ('FreeText', {'Текст': '&', 'x': 280, 'y': 426,
    #               'font_name': 'Montserrat-Bold',
    #               'font_size': 70, 'font_color': "#BBE02CFF", 'bold': False, 'align': 'left'}
    #  ),
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

]
page_frames_best_couple_product = {
    'template_1':
        (
            (0, (0, 85), (633, 940)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
            (1, (680, 554), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
            (2, (680, 106), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
}

elem_no_best_couple = [
    ('Spacer', {'width': 1, 'height': 11}),
    ('Image', {'Ключ в подборке': 'Путь к изображению средства 1', 'width': 640, 'height': 1280}),
    ('Spacer', {'width': 1, 'height': 26}),
    ('Image', {'Ключ в подборке': 'Путь к изображению средства 2', 'width': 640, 'height': 1280}),
    # ('FreeText', {'Текст': '&', 'x': 280, 'y': 426,
    #               'font_name': 'Montserrat-Bold',
    #               'font_size': 70, 'font_color': "#AC46F2FF", 'bold': False, 'align': 'left'}),
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

]
page_frames_no_best_couple_product = {
    'template_1':
        (
            (0, (0, 85), (633, 940)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
            (1, (680, 554), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
            (2, (680, 106), (574, 460)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
}

# 'Элементы и стили': elem_best_couple,
# 'Шаблоны страниц с фреймами': elem_no_best_couple,

# 'Элементы и стили': elem_no_best_couple,
# 'Шаблоны страниц с фреймами': page_frames_no_best_couple_product,

TEST_BEST_COUPLE_EXPECTED_RESULT = [
    {'Путь к изображению средства 1': Path(
        '00_base/products/00_img/r_co_dallas_biotin_thickening_shampoo_24320200017.jpg'),
        'Название средства 1': 'R+CO Dallas Biotin Thickening Shampoo',
        'Тип продукта 1': 'Шампунь с биотином для объема',
        'Артикул 1': 'артикул: 24320200017', 'Количество мера / цена 1': '251 мл / 5876 руб',
        'Путь к изображению средства 2': Path(
            '00_base/products/00_img/r_co_television_perfect_hair_masque_19760310342.jpg'),
        'Название средства 2': 'R+CO TELEVISION Perfect Hair Masque', 'Тип продукта 2': 'Маска для совершенства волос',
        'Артикул 2': 'артикул: 19760310342', 'Количество мера / цена 2': '147 мл / 8307 руб',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet_horizontal.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_dallas_biotin_thickening_shampoo_24320200017.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (1281, 85),
        'Координаты вставки бренд-линии': [(0, 0)], 'Размеры документа': (1280, 1024),
        'Элементы и стили': elem_no_best_couple,
        'Шаблоны страниц с фреймами': page_frames_no_best_couple_product,
    },
    {
        'Путь к изображению средства 1': Path(
            '00_base/products/00_img/r_co_atlantis_moisturizing_b5_shampoo_24320200015.jpg'),
        'Название средства 1': 'R+CO Atlantis Moisturizing B5 Shampoo',
        'Тип продукта 1': 'Шампунь для увлажнения с витамином В5', 'Артикул 1': 'артикул: 24320200015',
        'Количество мера / цена 1': '241 мл / 5876 руб', 'Путь к изображению средства 2': Path(
        '00_base/products/00_img/r_co_television_perfect_hair_conditioner_24320100036.jpg'),
        'Название средства 2': 'R+CO Television Perfect Hair Conditioner',
        'Тип продукта 2': 'Кондиционер для совершенства волос', 'Артикул 2': 'артикул: 24320100036',
        'Количество мера / цена 2': '241 мл / 6846 руб',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_green_horizontal.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_atlantis_moisturizing_b5_shampoo_24320200015.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (1281, 85),
        'Координаты вставки бренд-линии': [(0, 0)], 'Размеры документа': (1280, 1024),
        'Элементы и стили': elem_best_couple,
        'Шаблоны страниц с фреймами': page_frames_best_couple_product,
        'Путь к изображению галочки': Path('00_base/source/check/v2.png'),
    }
]
