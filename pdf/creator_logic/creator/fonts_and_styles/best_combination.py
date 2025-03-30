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
        alignment=TA_JUSTIFY,

    ),
    'BC_normal_2': ParagraphStyle(
        'BC_normal_2',
        fontName="DejaVuSans",
        alignment=TA_CENTER,
        fontSize=20,
        leading=20,
    ),
    'BC_bold_1': ParagraphStyle(
        'BC_bold_1',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_LEFT,
        leading=25,
    ),
}
