import os
from reportlab.lib.enums import (
    TA_LEFT,
    TA_RIGHT,
    TA_CENTER,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Размер страницы в пикселях
PAGE_WIDTH = 1024
PAGE_HEIGHT = 1280

# Регистрируем шрифты
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansBold", "DejaVuSans-Bold.ttf"))

# Стили текста
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'Title',
    fontName="DejaVuSansBold",
    fontSize=40,
    spaceBefore=50,
    spaceAfter=50,
    alignment=TA_CENTER,
    leftIndent=60,
    leading=45,
)
ratio_align_style = ParagraphStyle(
    'RightAlign',
    fontName="DejaVuSansBold",
    fontSize=25,
    alignment=TA_RIGHT,
)

bold_style = ParagraphStyle(
    'Bold',
    fontName="DejaVuSansBold",
    fontSize=25,
    spaceBefore=30,
    spaceAfter=20,
    alignment=TA_LEFT,
    leftIndent=70,
)
normal_style = ParagraphStyle(
    'Normal',
    fontName="DejaVuSans",
    fontSize=25,
    spaceBefore=30,
    spaceAfter=10,
    leftIndent=70,
    leading=25,
)


def add_brand_line(canvas, doc, brand_line_path):
    """Рисует бренд-линию слева перед остальным контентом."""
    canvas.drawImage(brand_line_path, 0, 0, width=80, height=PAGE_HEIGHT)



def add_product_image(elements, img_path):
    """Добавляет изображение продукта."""
    try:
        img = Image(img_path, width=PAGE_WIDTH, height=650)
        # Убираем отступ сверху
        elements.append(Spacer(1, -80))
        elements.append(img)
    except Exception as e:
        print(f"Ошибка загрузки изображения {img_path}: {e}")





def add_product_info(elements, product):
    """Добавляет текстовую информацию о продукте."""
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(product.get("Название", ""), title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"{product.get('Соотношение', '')}", ratio_align_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Плюсы:</b>", bold_style))
    elements.append(Paragraph(product.get("Плюсы", ""), normal_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Минусы:</b>", bold_style))
    elements.append(Paragraph(product.get("Минусы", ""), normal_style))


def create_pdf(list_with_info, output_folder="pdf_outputs"):
    """
    Функция для создания PDF-файлов с наложенной бренд-лентой
    :param list_with_info: список словарей с информацией о продуктах
    :param brand_line_path: путь к изображению бренд-ленты
    :param output_folder: папка для сохранения PDF
    """
    os.makedirs(output_folder, exist_ok=True)

    for product in list_with_info:
        product_name = product.get("Название", )
        safe_filename = product_name.replace(" ", "_").replace("/", "_") + ".pdf"
        output_file = os.path.join(output_folder, safe_filename)

        doc = SimpleDocTemplate(output_file, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        elements = []

        # Добавляем изображение
        add_product_image(elements, product.get("Ссылка на изображение в базе", ""))

        # Добавляем текстовую информацию
        add_product_info(elements, product)

        # разница в цветах ленты
        best_product = product.get('Лучшее средство')
        if best_product:
                # Генерируем PDF с наложением бренд-ленты
            doc.build(elements, onFirstPage=lambda c, d: add_brand_line(c, d, brand_line_path="imagine/border_green.jpg"),
                      onLaterPages=lambda c, d: add_brand_line(c, d, brand_line_path="imagine/border_green.jpg"))
        else:
            # Генерируем PDF с наложением бренд-ленты
            doc.build(elements,
                      onFirstPage=lambda c, d: add_brand_line(c, d, brand_line_path="imagine/border_fiolet.jpg"),
                      onLaterPages=lambda c, d: add_brand_line(c, d, brand_line_path="imagine/border_fiolet.jpg"))
        print(f"PDF сохранен: {output_file}")


if __name__ == "__main__":
    from pdf.utils import forming_indo_for_pdf
    from pdf.info_about_products import data_with_products

    result = forming_indo_for_pdf(data_with_products)
    create_pdf(list_with_info=result)
