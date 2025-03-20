from reportlab.lib.enums import (
    TA_CENTER,
    TA_RIGHT,
    TA_LEFT, TA_JUSTIFY,
)
from reportlab.lib.styles import ParagraphStyle

ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES = {
    'ACOP_title_1': ParagraphStyle(
        'ACOP_title_1',
        fontName="DejaVuSansBold",
        fontSize=25,
        alignment=TA_CENTER,
        leading=35,
    ),
    'ACOP_title_2': ParagraphStyle(
        'ACOP_title_2',
        fontName="DejaVuSansBold",
        fontSize=25,
        alignment=TA_CENTER,
    ),
    'ACOP_base_price_1': ParagraphStyle(
        'ACOP_base_price_1',
        fontName="DejaVuSans",
        fontSize=20,
        alignment=TA_CENTER,
    ),

    'ACOP_price_ratio_1': ParagraphStyle(
        'ACOP_price_ratio_1',
        fontName="DejaVuSans",
        fontSize=20,
        alignment=TA_CENTER,
    ),

    'ACOP_normal_1': ParagraphStyle(
        'ACOP_normal_1',
        fontName="DejaVuSans",
        fontSize=16,
        leading=20,
    ),
    'ACOP_normal_2': ParagraphStyle(
        'ACOP_normal_2',
        fontName="DejaVuSans",
        alignment=TA_CENTER,
        fontSize=20,
        leading=20,
    ),
    'ACOP_normal_3': ParagraphStyle(
        'ACOP_normal_3',
        fontName="DejaVuSans",
        alignment=TA_JUSTIFY,
        fontSize=15,
        leading=20,
        spaceAfter=20,

    ),
    'ACOP_bold_1': ParagraphStyle(
        'ACOP_bold_1',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_LEFT,
        leading=25,
    ),
    'ACOP_bold_2': ParagraphStyle(
        'ACOP_bold_2',
        fontName="DejaVuSansBold",
        fontSize=21,
        alignment=TA_CENTER,
        leading=25,
    ),
}
