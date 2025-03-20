from reportlab.lib.enums import (
    TA_CENTER,
    TA_RIGHT,
    TA_LEFT,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = (
    ("DejaVuSans", "00_base/source/fonts/DejaVuSans.ttf"),
    ("DejaVuSansBold", "00_base/source/fonts/DejaVuSans-Bold.ttf"),
)

for font in FONTS:
    pdfmetrics.registerFont(
        TTFont(
            name=font[0],
            filename=font[1]
        )
    )

BASE_PDF_STYLE = {
    'title_1': ParagraphStyle(
        'Title',
        fontName="DejaVuSansBold",
        fontSize=25,
        spaceBefore=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        leftIndent=50,
        leading=30,
    ),
    'base_price_1': ParagraphStyle(
        'RightAlign',
        fontName="DejaVuSansBold",
        fontSize=18,
        alignment=TA_RIGHT,
    ),
    'bold_1': ParagraphStyle(
        'Bold',
        fontName="DejaVuSansBold",
        fontSize=21,
        spaceBefore=10,
        spaceAfter=10,
        alignment=TA_LEFT,
        leftIndent=50,
    ),
    'normal_1': ParagraphStyle(
        'Normal',
        fontName="DejaVuSans",
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10,
        leftIndent=50,
        leading=20,
    ),
    'normal_2': ParagraphStyle(
        'Bold',
        fontName="DejaVuSans",
        fontSize=16,
        spaceBefore=10,
        spaceAfter=10,
        leftIndent=20,
        alignment=TA_CENTER,
    ),
}
