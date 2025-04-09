from reportlab.lib.enums import TA_JUSTIFY

from emojipy import Emoji
from reportlab.platypus import (
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm

import re


def convert_markdown_to_html(text: str) -> str:
    # **жирный** → <b>жирный</b>
    return re.sub(r'\*\*(.+?)\*\*', r'<font name="Montserrat-Bold">\1</font>', text)


def replace_emoji_html(text: str, size=16) -> str:
    """Преобразует emoji в <img ...> с цветными PNG."""
    Emoji.unicode_alt = False
    html = Emoji.to_image(text)
    html = html.replace('class="emojione"', f'height="{size}" width="{size}"')
    html = re.sub(r'alt="[^"]+"', '', html)  # Удаляем alt=""
    return html


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
