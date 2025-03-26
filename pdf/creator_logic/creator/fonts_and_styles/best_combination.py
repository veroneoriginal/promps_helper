from reportlab.lib.colors import HexColor
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_JUSTIFY, TA_RIGHT,
)
from reportlab.lib.styles import ParagraphStyle

BEST_COMBINATION_STYLES = {
    # Используем
    'BC_title_1': ParagraphStyle(
        'BC_title_1',
        fontName="DejaVuSansBold",
        fontSize=25,
        alignment=TA_CENTER,
        leading=35,
    ),
    # Используем
    'BC_title_2': ParagraphStyle(
        'BC_title_2',
        fontName="DejaVuSansBold",
        fontSize=25,
        alignment=TA_CENTER,
    ),
    # Используем
    'BC_base_price_right': ParagraphStyle(
        'BC_base_price_right',
        fontName="DejaVuSansBold",
        fontSize=20,
        alignment=TA_RIGHT,
    ),

    'BC_normal_1': ParagraphStyle(
        'BC_normal_1',
        fontName="DejaVuSans",
        fontSize=16,
        leading=20,
    ),
    'BC_normal_2': ParagraphStyle(
        'BC_normal_2',
        fontName="DejaVuSans",
        alignment=TA_CENTER,
        fontSize=20,
        leading=20,
    ),
    # Используем
    'BC_normal_3': ParagraphStyle(
        'BC_normal_3',
        fontName="DejaVuSans",
        alignment=TA_JUSTIFY,
        fontSize=15,
        leading=20,
        spaceAfter=20,

    ),
    'BC_bold_1': ParagraphStyle(
        'BC_bold_1',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_LEFT,
        leading=25,
    ),
    'BC_bold_2': ParagraphStyle(
        'BC_bold_2',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_CENTER,
        leading=25,
    ),
    'BC_ampersand': ParagraphStyle(
        'BC_ampersand',
        fontName="DejaVuSansBold",
        fontSize=50,
        alignment=TA_CENTER,
        leading=50,
        textColor=HexColor('#BBE02C')
    ),
}
