# pylint: skip-file

"""
Примеры структур для задачи "Лучшее средство без канцерогенов"
"""
from pathlib import Path

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_PDF_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf'
TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_JPG_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg'
FILE_PATH_TOOLS = '01_test_base/Средства для тестов.xlsx'

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_SELECTION_RESULT = {
    "best_product": "LOREAL PROFESSIONNEL Serioxyl Advanced",
    "product_1": {
        "title": "ALTEREGO ITALY Scalpego Balancing (артикул: 19000222491)",
        "plus": "Содержит сок алоэ и масло макадамии, которые могут способствовать увлажнению и питанию волос.",
        "minus": "Содержит сульфаты и консерванты, которые могут сушить волосы и вызывать раздражение кожи головы.",
        "best_product": False,
        "carcinogen": "Sodium c14-16 olefin sulfonate, Phenoxyethanol"
    },
    "product_2": {
        "title": "LOREAL PROFESSIONNEL Serioxyl Advanced (артикул: 19000146259)",
        "plus": "Содержит органические экстракты и масла, которые могут успокаивать кожу головы и укреплять волосы.",
        "minus": "Содержит сульфаты, которые могут сушить волосы и вызывать раздражение кожи головы.",
        "best_product": True,
        "carcinogen": "Нет"
    },
    "product_3": {
        "title": "NATURA SIBERICA Oblepikha (артикул: 19000141580)",
        "plus": "Содержит гидролизованный кератин, шелк и масла, которые глубоко питают и увлажняют волосы, укрепляют их структуру.",
        "minus": "Может быть более дорогим по сравнению с другими средствами.",
        "best_product": False,
        "carcinogen": "Sodium c14-16 olefin sulfonate, Phenoxyethanol"
    },
    "result": "Лучшим средством является LOREAL PROFESSIONNEL Serioxyl Advanced. Это средство содержит гидролизованный кератин, шелк и различные масла, которые обеспечивают глубокое питание и увлажнение волос, что соответствует запросу пользователя. Оно помогает восстановить водный баланс, укрепить структуру волос и защитить их от внешних воздействий, что делает волосы мягкими, гладкими и здоровыми. В отличие от других средств, оно не содержит агрессивных сульфатов, что делает его более подходящим для сухих и ломких волос."
}

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_COLLECTION_DATA = {
    'Задача': 'Лучшее средство без канцерогенов',
    'Категория': 'Шампуни',
}

elem = [
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
    ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BPWC_normal_2', 'Заглавными': True}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BPWC_title_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BPWC_base_price_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BPWC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BPWC_normal_1'}),
    ('Spacer', {'width': 1, 'height': 10}),
    ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BPWC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BPWC_normal_1'}),
    ('Spacer', {'width': 1, 'height': 10}),
    ('Paragraph', {'Текст': '<b>Канцерогены:</b>', 'Стиль': 'BPWC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Канцерогены', 'Стиль': 'BPWC_normal_1'}),
]
page_frames = {
    'template_1':
        (
            (0, (100, 0), (596, 966)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        )
}

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_EXPECTED_RESULT = [
    {
        'Артикул': 'артикул: 19000222491',
        'Канцерогены': 'Sodium c14-16 olefin sulfonate, Phenoxyethanol',
        'Количество мера / цена': '300 мл / 3390 рублей',
        'Минусы': 'Содержит сульфаты и консерванты, которые могут сушить волосы и '
                  'вызывать раздражение кожи головы.',
        'Название средства': 'ALTEREGO ITALY Scalpego Balancing',
        'Плюсы': 'Содержит сок алоэ и масло макадамии, которые могут способствовать '
                 'увлажнению и питанию волос.',
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/alterego_italy_scalpego_balancing_артикул_19000222491_.pdf'),
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь к изображению средства': Path(
            '00_base/products/00_img/alterego_italy_scalpego_balancing_19000222491.jpg'),
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Тип продукта': 'Балансирующий Шампунь для волос',
        'Шаблоны страниц с фреймами': page_frames,
        'Элементы и стили': elem,
    },
    {'Артикул': 'артикул: 19000146259',
     'Канцерогены': 'Нет',
     'Количество мера / цена': '300 мл / 2450 рублей',
     'Минусы': 'Содержит сульфаты, которые могут сушить волосы и вызывать '
               'раздражение кожи головы.',
     'Название средства': 'LOREAL PROFESSIONNEL Serioxyl Advanced',
     'Плюсы': 'Содержит органические экстракты и масла, которые могут успокаивать '
              'кожу головы и укреплять волосы.',
     'Путь для сохранения pdf-файла': Path(
         '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/loreal_professionnel_serioxyl_advanced_артикул_19000146259_.pdf'),
     'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_green.jpg'),
     'Путь к изображению средства': Path(
         '00_base/products/00_img/loreal_professionnel_serioxyl_advanced_19000146259.jpg'),
     'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
     'Размеры бренд-линии': (80, 1280),
     'Размеры документа': (1024, 1280),
     'Тип продукта': 'Шампунь для уплотнения волос',
     'Шаблоны страниц с фреймами': page_frames,
     'Элементы и стили': elem,
     },
    {
        'Артикул': 'артикул: 19000141580',
        'Канцерогены': 'Sodium c14-16 olefin sulfonate, Phenoxyethanol',
        'Количество мера / цена': '400 мл / 507 рублей',
        'Минусы': 'Может быть более дорогим по сравнению с другими средствами.',
        'Название средства': 'NATURA SIBERICA Oblepikha',
        'Плюсы': 'Содержит гидролизованный кератин, шелк и масла, которые глубоко '
                 'питают и увлажняют волосы, укрепляют их структуру.',
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/natura_siberica_oblepikha_артикул_19000141580_.pdf'),
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь к изображению средства': Path('00_base/products/00_img/natura_siberica_oblepikha_19000141580.jpg'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Тип продукта': 'Шампунь',
        'Шаблоны страниц с фреймами': page_frames,
        'Элементы и стили': elem,
    }
]
