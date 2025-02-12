from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def draw_background(canvas, doc):
    """Рисует фиолетовую полосу слева и текст 'BEAUTY HELPER'"""
    canvas.saveState()

    # Полоса слева (ширина 60 пикселей)
    stripe_width = 60
    canvas.setFillColor(colors.HexColor("#A78BFA"))  # Фиолетовый цвет
    canvas.rect(0, 0, stripe_width, A4[1], fill=True, stroke=False)

    # Текст "BEAUTY HELPER" вертикально
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVuSansBold", 12)
    canvas.rotate(90)  # Поворот текста
    canvas.drawString(10, -A4[0] + 20, "BEAUTY HELPER")
    canvas.rotate(-90)  # Возвращаем обратно

    canvas.restoreState()