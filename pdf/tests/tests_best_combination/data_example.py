# pylint: skip-file

"""
Примеры структур для задачи "Лучшее сочетание"
"""
from pathlib import Path

TEST_BEST_COMBINATION_PATH_PDF_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf'
TEST_BEST_COMBINATION_PATH_JPG_FILE = '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/04_jpg'
FILE_PATH_TOOLS = '01_test_base/Средства для тестов.xlsx'

TEST_BEST_COMBINATION_SELECTION_RESULT = {
    "origin_product": {
        "title": "R+CO Atlantis Moisturizing B5 Shampoo",
        "article": "24320200015",
        "plus": "Глубокое увлажнение благодаря провитамину В5, обволакивание волосяного стержня, естественный блеск, увлажнение и поддержание здорового уровня РН благодаря экстракту стволовых клеток опунции, укрепление и питание волос благодаря маслу рисовых отрубей.",
        "minus": "Может не обеспечивать достаточное питание и увлажнение для очень сухих и поврежденных волос, так как это шампунь, а не кондиционер или маска."
    },
    "result": "Для достижения наилучшего эффекта увлажнения и питания волос, а также для обеспечения мягкого и бережного очищения, рекомендуется использовать R+CO Atlantis Moisturizing B5 Conditioner в сочетании с исходным шампунем. Это средство дополнит увлажняющее действие шампуня и обеспечит дополнительное питание и защиту волос.",
    "product_1": {
        "title": "R+CO Television Perfect Hair Conditioner",
        "article": "24320100036",
        "plus": "Содержит экстракт ягод можжевельника и масло бабассу, не содержит парабенов, сульфатов, минеральных масел и продуктов животного происхождения.",
        "minus": "Может не обеспечивать достаточное увлажнение для очень сухих волос, так как основной акцент на натуральных компонентах и отсутствии агрессивных веществ.",
        "result": "Хотя это средство и подходит для поддержания здоровья волос, оно не обеспечивает такого уровня увлажнения и питания, как R+CO Atlantis Moisturizing B5 Conditioner, что важно для сухих волос.",
        "best_product": False
    },
    "product_2": {
        "title": "R+CO Atlantis Moisturizing B5 Conditioner",
        "article": "24320200016",
        "plus": "Содержит оливковое масло, масло рисовых отрубей и другие увлажняющие компоненты, которые обеспечивают глубокое увлажнение и питание волос, укрепляют их структуру и защищают от внешних воздействий.",
        "minus": "Может быть недостаточно легким для очень тонких волос, так как содержит масла, которые могут утяжелять волосы.",
        "result": "Это средство идеально дополняет исходный шампунь, так как они из одной серии и содержат схожие увлажняющие и питательные компоненты, что обеспечивает комплексный уход за сухими волосами.",
        "best_product": True
    },
    "product_3": {
        "title": "R+CO TELEVISION Perfect Hair Masque",
        "article": "19760310342",
        "plus": "Содержит экстракт тремеллы фукусовидной, масла кокоса, муру-муру, пекуи и абиссинии, которые обеспечивают глубокое увлажнение, питание и защиту волос.",
        "minus": "Может быть слишком тяжелым для частого использования, особенно для нормальных волос, так как это маска с высокой концентрацией масел.",
        "result": "Хотя маска обеспечивает глубокое увлажнение и питание, она может быть слишком тяжелой для частого использования, что не соответствует потребности в средстве для частого мытья.",
        "best_product": False
    }
}

TEST_BEST_COMBINATION_COLLECTION_DATA = {
    'Задача': 'Лучшее сочетание',
    'Категория': 'Шампуни',
}

elem_source_product = [
    ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
    ('Spacer', {'width': 1, 'height': 10}),
    ('FreeText',
     {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
      'font_name': 'DejaVuSans',
      'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
    ('FreeText',
     {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
      'font_name': 'DejaVuSans',
      'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
    ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Текст': '<b>Плюсы:</b>', 'Стиль': 'BC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Плюсы', 'Стиль': 'BC_normal_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Текст': '<b>Минусы:</b>', 'Стиль': 'BC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Минусы', 'Стиль': 'BC_normal_1'}),
]
page_frames_elem_source_product = {
    'template_1':
        (
            (0, (100, 0), (596, 966)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
}

elem_best_combination_product = [
    ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
    ('Spacer', {'width': 1, 'height': 10}),
    ('FreeText',
     {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
      'font_name': 'DejaVuSans',
      'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
    ('FreeText',
     {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
      'font_name': 'DejaVuSans',
      'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
    ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
    ('Spacer', {'width': 1, 'height': 40}),
    ('Paragraph', {'Текст': '<b>Почему выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
]
page_frames_best_combination_product = {
    'template_1':
        (
            (0, (100, 0), (596, 966)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
}

elem_unselect_combination_product = [
    ('Image', {'Ключ в подборке': 'Путь к изображению средства', 'width': 1024, 'height': 1280}),
    ('Spacer', {'width': 1, 'height': 10}),
    ('FreeText',
     {'Ключ в подборке': 'Артикул', 'x': 450, 'y': 500,
      'font_name': 'DejaVuSans',
      'font_size': 14, 'font_color': "#000000FF", 'bold': False, 'align': 'left'}),
    ('FreeText',
     {'Текст': 'Правообладатель изображения: https://goldapple.ru/', 'x': -30, 'y': 40,
      'font_name': 'DejaVuSans',
      'font_size': 10, 'font_color': "#1E1F2280", 'bold': False, 'align': 'left'}),
    ('Paragraph', {'Ключ в подборке': 'Тип продукта', 'Стиль': 'BC_normal_2'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Название средства', 'Стиль': 'BC_title_1'}),
    ('Spacer', {'width': 1, 'height': 20}),
    ('Paragraph', {'Ключ в подборке': 'Количество мера / цена', 'Стиль': 'BC_base_price_right'}),
    ('Spacer', {'width': 1, 'height': 40}),
    ('Paragraph', {'Текст': '<b>Почему НЕ выбрали это средство:</b>', 'Стиль': 'BC_bold_1'}),
    ('Spacer', {'width': 1, 'height': 15}),
    ('Paragraph', {'Ключ в подборке': 'Вывод', 'Стиль': 'BC_normal_1'}),
]
page_frames_unselect_combination_product = {
    'template_1':
        (
            (0, (100, 0), (596, 966)),  # Номер, Координаты левого нижнего угла, ширина и высота фрейма
        ),
}

TEST_BEST_COMBINATION_EXPECTED_RESULT = [
    {
        'Плюсы': 'Глубокое увлажнение благодаря провитамину В5, обволакивание волосяного стержня, естественный блеск, увлажнение и поддержание здорового уровня РН благодаря экстракту стволовых клеток опунции, укрепление и питание волос благодаря маслу рисовых отрубей.',
        'Минусы': 'Может не обеспечивать достаточное питание и увлажнение для очень сухих и поврежденных волос, так как это шампунь, а не кондиционер или маска.',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_green.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_atlantis_moisturizing_b5_shampoo_24320200015.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Элементы и стили': elem_source_product,
        'Шаблоны страниц с фреймами': page_frames_elem_source_product,
        'Название средства': 'R+CO Atlantis Moisturizing B5 Shampoo', 'Количество мера / цена': '241 мл / 5876 рублей',
        'Путь к изображению средства': Path(
            '00_base/products/00_img/r_co_atlantis_moisturizing_b5_shampoo_24320200015.jpg'),
        'Тип продукта': 'Шампунь для увлажнения с витамином В5', 'Артикул': 'артикул: 24320200015'},
    {
        'Вывод': 'Хотя это средство и подходит для поддержания здоровья волос, оно не обеспечивает такого уровня увлажнения и питания, как R+CO Atlantis Moisturizing B5 Conditioner, что важно для сухих волос.',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_television_perfect_hair_conditioner_24320100036.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Элементы и стили': elem_unselect_combination_product,
        'Шаблоны страниц с фреймами': page_frames_unselect_combination_product,
        'Название средства': 'R+CO Television Perfect Hair Conditioner',
        'Количество мера / цена': '241 мл / 6846 рублей', 'Путь к изображению средства': Path(
        '00_base/products/00_img/r_co_television_perfect_hair_conditioner_24320100036.jpg'),
        'Тип продукта': 'Кондиционер для совершенства волос', 'Артикул': 'артикул: 24320100036'},
    {
        'Вывод': 'Это средство идеально дополняет исходный шампунь, так как они из одной серии и содержат схожие увлажняющие и питательные компоненты, что обеспечивает комплексный уход за сухими волосами.',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_green.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_atlantis_moisturizing_b5_conditioner_24320200016.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Элементы и стили': elem_best_combination_product,
        'Шаблоны страниц с фреймами': page_frames_best_combination_product,
        'Название средства': 'R+CO Atlantis Moisturizing B5 Conditioner',
        'Количество мера / цена': '241 мл / 5876 рублей', 'Путь к изображению средства': Path(
        '00_base/products/00_img/r_co_atlantis_moisturizing_b5_conditioner_24320200016.jpg'),
        'Тип продукта': 'Кондиционер для увлажнения с витамином В5', 'Артикул': 'артикул: 24320200016'},
    {
        'Вывод': 'Хотя маска обеспечивает глубокое увлажнение и питание, она может быть слишком тяжелой для частого использования, что не соответствует потребности в средстве для частого мытья.',
        'Путь к изображению бренд-линии': Path('00_base/source/imagine_border/border_fiolet.jpg'),
        'Путь для сохранения pdf-файла': Path(
            '01_test_base/00_info_for_post/22_22_2222/100_Шампуни/00_source/03_pdf/r_co_television_perfect_hair_masque_19760310342.pdf'),
        'Класс шаблона': 'PDFBaseDocTemplateWithBrandLine', 'Размеры бренд-линии': (80, 1280),
        'Размеры документа': (1024, 1280),
        'Элементы и стили': elem_unselect_combination_product,
        'Шаблоны страниц с фреймами': page_frames_unselect_combination_product,
        'Название средства': 'R+CO TELEVISION Perfect Hair Masque', 'Количество мера / цена': '147 мл / 8307 рублей',
        'Путь к изображению средства': Path(
            '00_base/products/00_img/r_co_television_perfect_hair_masque_19760310342.jpg'),
        'Тип продукта': 'Маска для совершенства волос', 'Артикул': 'артикул: 19760310342'}
]
