from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pdf.creator_logic.creator.fonts_and_styles.analysis_composition_one_product import (
    ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES,
)
from pdf.creator_logic.creator.fonts_and_styles.best_product import BEST_PRODUCT_STYLES

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

PDF_STYLE = {}
PDF_STYLE.update(BEST_PRODUCT_STYLES)
PDF_STYLE.update(ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES)
