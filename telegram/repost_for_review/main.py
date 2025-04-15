import os
import re
from pathlib import Path

import markdown2
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telebot.types import InputMediaPhoto

load_dotenv()
BOT_TOKEN = os.getenv('BH_POST_FOR_REVIEW_BOT_TOKEN')
CHAT_ID = os.getenv('REVIEW_POST_CHAT_ID')
REPOST_DETAILED_TEXT = os.getenv('REPOST_DETAILED_TEXT')

bot = telebot.TeleBot(BOT_TOKEN)


def md_to_telegram_html(md_text: str) -> str:
    """
    Переконвертирует Markdown в валидный HTML для Telegram
    """

    check_pattern = (
        ":—–.,;!?)»abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуф"
        "хцчшщэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХ"
        "ЦЧШЩЭЮЯ0123456789"
    )

    # 1. Заменяем \n на маркер
    md_text = md_text.replace('\n', '[[[NL]]]')

    # 2. Markdown -> HTML
    html = markdown2.markdown(md_text)

    # 3. Чистим HTML от лишних тегов
    allowed_tags = {"b", "strong", "i", "em", "u", "s", "del", "ins", "a", "code", "pre"}
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all():
        if tag.name not in allowed_tags:
            tag.unwrap()

    # 4. Получаем строку
    clean_html = soup.decode(formatter=None)

    # 5. Удаляем <p>, <li>
    clean_html = (
        clean_html.replace("<p>", "")
        .replace("</p>", "\n\n")
    )
    clean_html = (
        clean_html.replace("<li>", "- ")
        .replace("</li>", "\n")
    )

    # 6. Разбиваем построчно и корректируем поведение вокруг </strong> и </a>
    lines = clean_html.splitlines()
    result_lines = []
    for i, line in enumerate(lines):
        result_lines.append(line)
        # Если строка заканчивается на </strong> или </a> и
        # следующая НЕ начинается с ":" или алфавита — вставляем \n
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if line.strip().endswith(("</strong>", "</a>")) and (
                    not next_line or next_line[0] not in check_pattern
            ):
                result_lines.append("")

    # 7. Склеиваем обратно
    clean_html = "\n".join(result_lines)

    # 8. Возвращаем переносы
    clean_html = clean_html.replace('[[[NL]]]', '\n')

    # 9. Чистим лишние пустые строки
    clean_html = re.sub(r'\n{3,}', '\n\n', clean_html)

    return clean_html.strip()


def send_images_and_text(
        images: list[str],
        chat_id: str,
        _bot: telebot.TeleBot,
        chunk_size: int = 10
) -> None:
    """
    Отправляет изображения чанками по 10 и текст в конце.

    :param images: список путей к изображениям
    :param chat_id: ID чата Telegram
    :param _bot: экземпляр TeleBot
    :param chunk_size: максимальное количество изображений за один вызов send_media_group
    """

    for i in range(0, len(images), chunk_size):
        chunk = images[i:i + chunk_size]
        media_group = []

        for img_path in chunk:
            with open(img_path, 'rb') as img_file:
                media = InputMediaPhoto(img_file.read())
                media_group.append(media)

        _bot.send_media_group(chat_id, media_group)


def send_post_from_folder(
        path_to_markdown_folder: str,
        images_folder: str
) -> None:
    """
    Отправляет пост в виде медиа-группы с изображениями и подписью из markdown файла.

    :param path_to_markdown_folder: путь к .md-файлу с текстом поста
    :param images_folder: путь к папке с изображениями
    """

    if REPOST_DETAILED_TEXT:
        file_name = 'text_for_review_post_detailed.md'
    else:
        file_name = 'text_for_review_post_short.md'

    markdown_file_path = Path(path_to_markdown_folder) / 'telegram_review' / file_name
    # читаем текст из markdown-файла
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        post_text = f.read()
        telegram_ready_text = md_to_telegram_html(post_text)

        # собираем список всех .jpg файлов в указанной папке
        images = sorted([
            os.path.join(images_folder, file)
            for file in os.listdir(images_folder)
            if file.lower().endswith('.jpg')
        ])

        send_images_and_text(images=images, chat_id=CHAT_ID, _bot=bot)

        bot.send_message(CHAT_ID, telegram_ready_text, parse_mode='HTML')
