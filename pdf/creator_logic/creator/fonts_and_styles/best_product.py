from reportlab.lib.enums import (
    TA_CENTER,
    TA_RIGHT,
    TA_LEFT, TA_JUSTIFY,
)
from reportlab.lib.styles import ParagraphStyle

BEST_PRODUCT_STYLES = {
    'BP_title_1': ParagraphStyle(
        'BP_title_1',
        fontName="DejaVuSansBold",
        fontSize=25,
        alignment=TA_CENTER,
        leading=35,
    ),
    'BP_base_price_1': ParagraphStyle(
        'BP_base_price_1',
        fontName="DejaVuSansBold",
        fontSize=18,
        alignment=TA_RIGHT,
    ),
    'BP_bold_1': ParagraphStyle(
        'BP_bold_1',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_LEFT,
    ),

    'BP_normal_1': ParagraphStyle(
        'BP_normal_1',
        fontName="DejaVuSans",
        fontSize=16,
        leading=20,
        alignment=TA_JUSTIFY,
    ),

    'BP_normal_2': ParagraphStyle(
        'BP_normal_2',
        fontName="DejaVuSans",
        alignment=TA_CENTER,
        fontSize=20,
        leading=20,
    ),
}
