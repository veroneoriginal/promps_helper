# pylint: disable=E0611: no-name-in-module

from reportlab.lib.enums import TA_JUSTIFY

from reportlab.platypus import (
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm

from pdf.utils import convert_markdown_to_html, replace_emoji_html


def create_emodji_flowables(text) -> list[Spacer | Paragraph]:
    flowables = []

    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        name="EmojiStyle",
        parent=styles["Normal"],
        fontName="Montserrat-Regular",
        fontSize=15,
        leading=17,
        alignment=TA_JUSTIFY
    )

    # === 3. Обработка текста ===
    for block in text.strip().split("\n"):
        block = block.strip()
        if not block:
            flowables.append(Spacer(1, 5 * mm))
            continue
        html = convert_markdown_to_html(block)
        html = replace_emoji_html(html, size=14)
        flowables.append(Paragraph(html, style))
        flowables.append(Spacer(1, 2 * mm))
    return flowables
