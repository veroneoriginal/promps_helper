from reportlab.lib.enums import (
    TA_CENTER,
)
from reportlab.lib.styles import ParagraphStyle

BEST_COUPLE_STYLES = {
    # Используем
    'BEST_COUPLE_title_1': ParagraphStyle(
        'BEST_COUPLE_title_1',
        fontName="Montserrat-SemiBold",
        fontSize=24,
        alignment=TA_CENTER,
        leading=35,
    ),
    # Используем
    'BEST_COUPLE_base_price': ParagraphStyle(
        'BEST_COUPLE_base_price_right',
        fontName="Montserrat-SemiBold",
        fontSize=22,
        alignment=TA_CENTER,
    ),

    'BEST_COUPLE_normal_1': ParagraphStyle(
        'BEST_COUPLE_normal_1',
        fontName="Montserrat-Medium",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,

    ),
    'BEST_COUPLE_bold_1': ParagraphStyle(
        'BEST_COUPLE_bold_1',
        fontName="Montserrat-Medium",
        fontSize=17,
        alignment=TA_CENTER,
        leading=18,
    ),
}
