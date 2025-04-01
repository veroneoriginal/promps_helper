from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pdf.creator_logic.creator.fonts_and_styles.analogue import ANALOGUE_STYLES
from pdf.creator_logic.creator.fonts_and_styles.analysis_composition_one_product import (
    ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES,
)
from pdf.creator_logic.creator.fonts_and_styles.best_combination import BEST_COMBINATION_STYLES
from pdf.creator_logic.creator.fonts_and_styles.best_couple import BEST_COUPLE_STYLES
from pdf.creator_logic.creator.fonts_and_styles.best_product import BEST_PRODUCT_STYLES
from pdf.creator_logic.creator.fonts_and_styles.best_product_without_carcinogens import (
    BEST_PRODUCT_WITHOUT_CARCINOGENS_STYLES,
)

FONTS = (
    ("DejaVuSans", "00_base/source/fonts/DejaVuSans.ttf"),
    ("DejaVuSansBold", "00_base/source/fonts/DejaVuSans-Bold.ttf"),
    ("Montserrat-Medium", "00_base/source/fonts/Montserrat-Medium.ttf"),
    ("Montserrat-Bold", "00_base/source/fonts/Montserrat-Bold.ttf"),
    ("Montserrat-Regular", "00_base/source/fonts/Montserrat-Regular.ttf"),
    ("Montserrat-SemiBold", "00_base/source/fonts/Montserrat-SemiBold.ttf"),
)

for font in FONTS:
    pdfmetrics.registerFont(
        TTFont(
            name=font[0],
            filename=font[1]
        )
    )

PDF_STYLE = {}
PDF_ADDITIONAL_STYLES = (
    BEST_PRODUCT_STYLES,
    ANALYSIS_COMPOSITION_ONE_PRODUCT_STYLES,
    BEST_PRODUCT_WITHOUT_CARCINOGENS_STYLES,
    BEST_COMBINATION_STYLES,
    BEST_COUPLE_STYLES,
    ANALOGUE_STYLES,
)
for style in PDF_ADDITIONAL_STYLES:
    PDF_STYLE.update(style)
