import os

import telebot
from dotenv import load_dotenv
# создаём список InputMediaPhoto
from telebot.types import InputMediaPhoto

load_dotenv()
BOT_TOKEN = os.getenv('BH_POST_FOR_REVIEW_BOT_TOKEN')
CHAT_ID = os.getenv('REVIEW_POST_CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

# список картинок (можно использовать file_id, URL или путь к локальному файлу)
images = [
    '00_base/00_info_for_post/13_04_25/18_шампуни_кондиционеры_бесплатная/05_jpg/r_co_atlantis_moisturizing_b5_conditioner_24320200016_page_1.jpg',
    '00_base/00_info_for_post/13_04_25/18_шампуни_кондиционеры_бесплатная/05_jpg/r_co_atlantis_moisturizing_b5_shampoo_24320200015_page_1.jpg',
    '00_base/00_info_for_post/13_04_25/18_шампуни_кондиционеры_бесплатная/05_jpg/r_co_television_perfect_hair_conditioner_24320100036_page_1.jpg',
    '00_base/00_info_for_post/13_04_25/18_шампуни_кондиционеры_бесплатная/05_jpg/r_co_television_perfect_hair_masque_19760310342_page_1.jpg',
]

media_group = [
    InputMediaPhoto(open(image_path, 'rb')) for image_path in images
]

post = """
💄 Средства из подборки:
[R+CO Atlantis Moisturizing B5 Shampoo](https://dzen.ru/?yredirect=true): арт. 24320200015
R+CO Television Perfect Hair Conditioner: арт. 24320100036
R+CO Atlantis Moisturizing B5 Conditioner: арт. 24320200016
R+CO TELEVISION Perfect Hair Masque: арт. 19760310342
"""

# необязательно, можно добавить подпись только к первому изображению
media_group[0].caption = post
media_group[0].parse_mode = 'MARKDOWN'

# отправляем альбом
bot.send_media_group(CHAT_ID, media_group)
