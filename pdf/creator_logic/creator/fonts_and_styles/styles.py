from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pdf.creator_logic.creator.fonts_and_styles.analysis_composition_one_product import (
    ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES,
)
from pdf.creator_logic.creator.fonts_and_styles.best_combination import BEST_COMBINATION_STYLES
from pdf.creator_logic.creator.fonts_and_styles.best_product import BEST_PRODUCT_STYLES
from pdf.creator_logic.creator.fonts_and_styles.best_product_without_carcinogens import (
    BEST_PRODUCT_WITHOUT_CARCINOGENS_STYLES,
)

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

BASE_STYLES = {
    'product_article': ParagraphStyle(
        'product_article',
        fontName="DejaVuSans",
        fontSize=15,
        alignment=TA_LEFT,
    ),
}

PDF_STYLE = {}
PDF_STYLE.update(BASE_STYLES)
PDF_STYLE.update(BEST_PRODUCT_STYLES)
PDF_STYLE.update(ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES)
PDF_STYLE.update(BEST_PRODUCT_WITHOUT_CARCINOGENS_STYLES)
PDF_STYLE.update(BEST_COMBINATION_STYLES)
