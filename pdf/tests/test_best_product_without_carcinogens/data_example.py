# pylint: skip-file

"""
Примеры структур для задачи "Лучшее средство без канцерогенов"
"""
from pathlib import Path

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_PDF_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf'
TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_PATH_JPG_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg'
FILE_PATH_TOOLS = '01_test_base/Средства для тестов.xlsx'

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_SELECTION_RESULT = {
    "product_1": {
        "title": "ALTEREGO ITALY Scalpego Balancing",
        "article": "19000222491",
        "plus": "Содержит сок алоэ и масло макадамии, которые могут способствовать увлажнению и питанию волос.",
        "minus": "Содержит сульфаты и консерванты, которые могут сушить волосы и вызывать раздражение кожи головы.",
        "best_product": False,
        "carcinogen": "Sodium c14-16 olefin sulfonate, Phenoxyethanol",
        "influence_of_carcinogens": "Benzyl Alcohol может вызывать раздражение кожи и аллергические реакции. Benzyl Benzoate и Benzyl Cinnamate могут быть потенциальными аллергенами и раздражителями."
    },
    "product_2": {
        "title": "LOREAL PROFESSIONNEL Serioxyl Advanced",
        "article": "19000146259",
        "plus": "Содержит органические экстракты и масла, которые могут успокаивать кожу головы и укреплять волосы.",
        "minus": "Содержит сульфаты, которые могут сушить волосы и вызывать раздражение кожи головы.",
        "best_product": True,
        "carcinogen": "",
        "influence_of_carcinogens": ""
    },
    "product_3": {
        "title": "NATURA SIBERICA Oblepikha",
        "article": "19000141580",
        "plus": "Содержит гидролизованный кератин, шелк и масла, которые глубоко питают и увлажняют волосы, укрепляют их структуру.",
        "minus": "Может быть более дорогим по сравнению с другими средствами.",
        "best_product": False,
        "carcinogen": "Sodium c14-16 olefin sulfonate, Phenoxyethanol",
        "influence_of_carcinogens": "Benzyl Alcohol может вызывать раздражение кожи и аллергические реакции. Benzyl Benzoate и Benzyl Cinnamate могут быть потенциальными аллергенами и раздражителями."
    },
    "result": "Лучшим средством является LOREAL PROFESSIONNEL Serioxyl Advanced. Это средство содержит гидролизованный кератин, шелк и различные масла, которые обеспечивают глубокое питание и увлажнение волос, что соответствует запросу пользователя. Оно помогает восстановить водный баланс, укрепить структуру волос и защитить их от внешних воздействий, что делает волосы мягкими, гладкими и здоровыми. В отличие от других средств, оно не содержит агрессивных сульфатов, что делает его более подходящим для сухих и ломких волос."
}

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_COLLECTION_DATA = {
    'Задача': 'Лучшее средство без канцерогенов',
    'Категория': 'Шампуни',
}

best_elem = [
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
    ('NextPageTemplate', {'template_id': 'template_2'}),
    ('PageBreak', {}),
    ('Paragraph', {'Текст': '<b>Влияние канцерогенов:</b>', 'Стиль': 'BPWC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 30}),
    ('Paragraph', {'Ключ в подборке': 'Влияние канцерогенов', 'Стиль': 'BPWC_normal_1'}),
]
page_frames = {
    'template_1':
        (
            (0, (133, 0), (794, 1288)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
    'template_2':
        (
            (1, (133, 0), (794, 1220)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        )
}

no_best_elem = [
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
    ('NextPageTemplate', {'template_id': 'template_2'}),
    ('PageBreak', {}),
    ('Paragraph', {'Текст': '<b>Влияние канцерогенов:</b>', 'Стиль': 'BPWC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 30}),
    ('Paragraph', {'Ключ в подборке': 'Влияние канцерогенов', 'Стиль': 'BPWC_normal_1'}),
]

TEST_BEST_PRODUCT_WITHOUT_CARCINOGENS_EXPECTED_RESULT = [
    {
        'Артикул': 'артикул: 19000222491',
        'Канцерогены': 'Sodium c14-16 olefin sulfonate, Phenoxyethanol',
        'Влияние канцерогенов': 'Benzyl Alcohol может вызывать раздражение кожи и '
                                'аллергические реакции. Benzyl Benzoate и Benzyl '
                                'Cinnamate могут быть потенциальными аллергенами и '
                                'раздражителями.',

        'Количество мера / цена': '300 мл / 3390 руб',
        'Минусы': 'Содержит сульфаты и консерванты, которые могут сушить волосы и '
                  'вызывать раздражение кожи головы.',
        'Название средства': 'ALTEREGO ITALY Scalpego Balancing',
        'Плюсы': 'Содержит сок алоэ и масло макадамии, которые могут способствовать '
                 'увлажнению и питанию волос.',
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/alterego_italy_scalpego_balancing_19000222491.pdf'),
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь к изображению средства': Path(
            '00_base/products/00_img/alterego_italy_scalpego_balancing_19000222491.jpg'),
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Тип продукта': 'Балансирующий Шампунь для волос',
        'Шаблоны страниц с фреймами': page_frames,
        'Элементы и стили': no_best_elem,
    },
    {'Артикул': 'артикул: 19000146259',
     'Канцерогены': 'Не найдены',
     'Влияние канцерогенов': 'Не найдены',
     'Количество мера / цена': '300 мл / 2450 руб',
     'Минусы': 'Содержит сульфаты, которые могут сушить волосы и вызывать '
               'раздражение кожи головы.',
     'Название средства': 'LOREAL PROFESSIONNEL Serioxyl Advanced',
     'Плюсы': 'Содержит органические экстракты и масла, которые могут успокаивать '
              'кожу головы и укреплять волосы.',
     'Путь для сохранения pdf-файла': Path(
         '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/loreal_professionnel_serioxyl_advanced_19000146259.pdf'),
     'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_green.jpg'),
     'Путь к изображению галочки': Path('00_base/source/check/v2.png'),
     'Путь к изображению средства': Path(
         '00_base/products/00_img/loreal_professionnel_serioxyl_advanced_19000146259.jpg'),
     'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
     'Размеры бренд-линии': (85, 1280),
     'Координаты вставки бренд-линии': [(0, 0), ],
     'Размеры документа': (1024, 1280),
     'Тип продукта': 'Шампунь для уплотнения волос',
     'Шаблоны страниц с фреймами': page_frames,
     'Элементы и стили': best_elem,
     },
    {
        'Артикул': 'артикул: 19000141580',
        'Канцерогены': 'Sodium c14-16 olefin sulfonate, Phenoxyethanol',
        'Влияние канцерогенов': 'Benzyl Alcohol может вызывать раздражение кожи и '
                                'аллергические реакции. Benzyl Benzoate и Benzyl '
                                'Cinnamate могут быть потенциальными аллергенами и '
                                'раздражителями.',

        'Количество мера / цена': '400 мл / 507 руб',
        'Минусы': 'Может быть более дорогим по сравнению с другими средствами.',
        'Название средства': 'NATURA SIBERICA Oblepikha',
        'Плюсы': 'Содержит гидролизованный кератин, шелк и масла, которые глубоко '
                 'питают и увлажняют волосы, укрепляют их структуру.',
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/natura_siberica_oblepikha_19000141580.pdf'),
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь к изображению средства': Path('00_base/products/00_img/natura_siberica_oblepikha_19000141580.jpg'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine',
        'Размеры бренд-линии': (85, 1280),
        'Координаты вставки бренд-линии': [(0, 0), ],
        'Размеры документа': (1024, 1280),
        'Тип продукта': 'Шампунь',
        'Шаблоны страниц с фреймами': page_frames,
        'Элементы и стили': no_best_elem,
    }
]
