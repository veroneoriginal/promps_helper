import os
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image
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

def add_product_image(elements, img_path):
    """Добавляет изображение продукта."""
    try:
        img = Image(img_path, width=PAGE_WIDTH, height=650)
        # Сдвигаем изображение вверх, если нужно (отрицательный Spacer)
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
    Создает PDF-файлы с наложенной бренд‑линей поверх основного контента.
    :param list_with_info: список словарей с информацией о продуктах.
    :param output_folder: папка для сохранения PDF.
    """
    os.makedirs(output_folder, exist_ok=True)

    for product in list_with_info:
        product_name = product.get("Название", "product")
        safe_filename = product_name.replace(" ", "_").replace("/", "_") + ".pdf"
        output_file = os.path.join(output_folder, safe_filename)

        # Выбираем нужную бренд‑линию по условию
        if product.get('Лучшее средство'):
            brand_line = "imagine/border_green.jpg"
        else:
            brand_line = "imagine/border_fiolet.jpg"

        # Создаем BaseDocTemplate
        doc = BaseDocTemplate(output_file, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        # Создаем фрейм для основных элементов (flowables)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')

        # Функция, которая отрисовывает бренд‑линию поверх контента.
        # Здесь бренд‑линия занимает всю высоту страницы,
        # но мы сдвигаем её так, чтобы верхняя грань совпадала с верхом страницы.
        def draw_brand_line(canvas, doc):
            try:
                desired_height = PAGE_HEIGHT  # занимает всю высоту страницы
                # Вычисляем координату y, чтобы верх картинки был на верхнем крае страницы:
                y = PAGE_HEIGHT - desired_height  # в данном случае y=0, но если захотите меньшую высоту – поменяйте desired_height
                canvas.drawImage(
                    brand_line,
                    0,
                    y,
                    width=80,
                    height=desired_height,
                    preserveAspectRatio=True
                )
            except Exception as e:
                print(f"Ошибка при отрисовке бренд-линии {brand_line}: {e}")

        # Создаем PageTemplate с использованием onPageEnd
        template = PageTemplate(id='normal', frames=[frame], onPageEnd=draw_brand_line)
        doc.addPageTemplates([template])

        flowables = []
        add_product_image(flowables, product.get("Ссылка на изображение в базе", ""))
        add_product_info(flowables, product)

        doc.build(flowables)
        print(f"PDF сохранен: {output_file}")

if __name__ == "__main__":
    # Предполагается, что данные о продуктах импортируются из ваших модулей
    from pdf.utils import forming_indo_for_pdf
    from pdf.info_about_products import data_with_products

    result = forming_indo_for_pdf(data_with_products)
    create_pdf(list_with_info=result)
