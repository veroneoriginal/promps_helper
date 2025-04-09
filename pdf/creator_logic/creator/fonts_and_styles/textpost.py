from reportlab.lib.enums import (
    TA_CENTER,
    TA_RIGHT,
    TA_LEFT, TA_JUSTIFY,
)
from reportlab.lib.styles import ParagraphStyle

TEXTPOST_STYLES = {
    'EmojiStyle': ParagraphStyle(
        'EmojiStyle',
        fontName="Montserrat-Regular",
        fontSize=15,
        leading=17,
        alignment=TA_JUSTIFY,
    ),
}
