from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, SimpleDocTemplate

def add_full_width_image(image_path, output_pdf):
    """Добавляет изображение на всю ширину A4 с сохранением пропорций"""

    # Создаем PDF-документ
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)

    # Максимальная ширина изображения (размер страницы)
    max_width = A4[0]

    # Загружаем изображение
    img = Image(image_path)

    # Вычисляем новую высоту, сохраняя пропорции
    aspect_ratio = img.imageHeight / img.imageWidth
    new_height = max_width * aspect_ratio  # Высота рассчитывается автоматически

    # Устанавливаем новое разрешение
    img.drawWidth = max_width
    img.drawHeight = new_height

    # Создаем PDF с изображением
    doc.build([img]*1)
    print(f"PDF сохранен: {output_pdf}")

# Пример использования
image_path = "00_base/01_products/00_img/_for_curly_hair.jpg"
output_pdf = "pdf_outputs/output.pdf"
add_full_width_image(image_path, output_pdf)