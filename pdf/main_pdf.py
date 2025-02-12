import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Frame,
    PageTemplate,
    Table,
    TableStyle,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pdf.info_about_products import data_with_products
from pdf.utils import forming_indo_for_pdf
from pdf.styles_for_standart_picture import draw_background

# Регистрируем шрифты
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansBold", "DejaVuSans-Bold.ttf"))

# Стили текста
styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', fontName="DejaVuSansBold", fontSize=18, spaceAfter=10, alignment=TA_LEFT)
normal_style = ParagraphStyle('Normal', fontName="DejaVuSans", fontSize=12, spaceAfter=8)
bold_style = ParagraphStyle('Bold', fontName="DejaVuSansBold", fontSize=12, spaceAfter=8)
right_align_style = ParagraphStyle('RightAlign', fontName="DejaVuSansBold", fontSize=12, alignment=TA_RIGHT)


def create_pdf(list_with_info, output_folder="pdf_outputs"):
    """
    Функция для создания pdf-файла

    :param list_with_info: список словарей со всей средствами и информацией для картинки
    """
    # Создаем папку для PDF, если её нет
    os.makedirs(output_folder, exist_ok=True)

    for product in list_with_info:
        product_name = product.get("Название", "Без названия")
        safe_filename = product_name.replace(" ", "_").replace("/", "_") + ".pdf"
        output_file = os.path.join(output_folder, safe_filename)

        # Создаем PDF-документ
        doc = SimpleDocTemplate(output_file, pagesize=A4)

        # Задаем размеры блоков
        image_height = 450  # Фиксированная высота изображения
        text_start_y = A4[1] - image_height - 50  # Начало текста ниже изображения

        # Фрейм для изображения (сверху)
        image_frame = Frame(0, A4[1] - image_height, A4[0],
                            image_height,
                            leftPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            bottomPadding=0)

        # Фрейм для текста (ниже изображения)
        text_frame = Frame(50, 50, A4[0] - 100, text_start_y - 50)

        # Создаем шаблон страницы с двумя фреймами
        template = PageTemplate(frames=[image_frame, text_frame])
        doc.addPageTemplates([template])

        elements = []

        # Добавляем изображение (на всю ширину, фиксированная высота)
        img_path = product.get("Ссылка на изображение в базе", "")
        try:
            img = Image(img_path, width=A4[0], height=image_height)
            elements.append(img)
        except Exception as e:
            print(f"Ошибка загрузки изображения {img_path}: {e}")

        # Добавляем заголовок
        elements.append(Paragraph(product.get("Название", ""), title_style))
        elements.append(Spacer(1, 10))

        # Соотношение (объем / цена)
        elements.append(Paragraph(f"{product.get('Соотношение', '')}", right_align_style))
        elements.append(Spacer(1, 10))

        # Плюсы
        elements.append(Paragraph("<b>Плюсы:</b>", bold_style))
        elements.append(Paragraph(product.get("Плюсы", ""), normal_style))
        elements.append(Spacer(1, 8))

        # Минусы
        elements.append(Paragraph("<b>Минусы:</b>", bold_style))
        elements.append(Paragraph(product.get("Минусы", ""), normal_style))

        # Генерируем PDF
        doc.build(elements)
        print(f"PDF сохранен: {output_file}")


if __name__ == "__main__":
    result = forming_indo_for_pdf(data_with_products)
    create_pdf(list_with_info=result)
