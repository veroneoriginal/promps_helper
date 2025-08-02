from reportlab.lib.enums import (
    TA_CENTER, TA_JUSTIFY, TA_LEFT,
)
from reportlab.lib.styles import ParagraphStyle

ANALOGUE_STYLES = {
    # Используем
    'ANALOGUE_title_1': ParagraphStyle(
        'ANALOGUE_title_1',
        fontName="Montserrat-SemiBold",
        fontSize=22,
        alignment=TA_CENTER,
        leading=32,
    ),
    # Используем
    'ANALOGUE_base_price': ParagraphStyle(
        'ANALOGUE_base_price_right',
        fontName="Montserrat-SemiBold",
        fontSize=20,
        alignment=TA_CENTER,
    ),

    'ANALOGUE_normal_1': ParagraphStyle(
        'ANALOGUE_normal_1',
        fontName="Montserrat-Medium",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,

    ),
    'ANALOGUE_text_title': ParagraphStyle(
        'ANALOGUE_bold_1',
        fontName="Montserrat-SemiBold",
        fontSize=19,
        alignment=TA_LEFT,
        leading=25,
    ),
    'ANALOGUE_text': ParagraphStyle(
        'ANALOGUE_text',
        fontName="Montserrat-Regular",
        fontSize=15,
        leading=17,
        alignment=TA_JUSTIFY,

    ),
    'ANALOGUE_bold_1': ParagraphStyle(
        'ANALOGUE_bold_1',
        fontName="Montserrat-Medium",
        fontSize=15,
        alignment=TA_CENTER,
        leading=16,
    ),
}
