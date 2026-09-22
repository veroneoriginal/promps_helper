from pathlib import Path

SCHEME_FOR_FOLDERS_NAME = [
    '00_json_scheme',
    '01_prompt',
    '02_answer_gpt',
    '03_token_price',
    '04_pdf',
    '05_jpg',
    '06_text'
]

# Базовый путь к ассетам
BASE_PATH_TO_ASSETS = Path("./source/assets/")
# Зеленая галочка
GREEN_ACCEPT_CHECK_IMAGE_PATH = BASE_PATH_TO_ASSETS / 'check/v2.png'
# Вертикальные бренд-линии
BRAND_LINE_BASE_PATH = BASE_PATH_TO_ASSETS / 'imagine_border/'

GREEN_VERTICAL_BRAND_LINE_PATH = BRAND_LINE_BASE_PATH / 'border_green.jpg'
ORANGE_LIGHT_VERTICAL_BRAND_LINE_PATH = BRAND_LINE_BASE_PATH / 'border_orange_light.jpg'
FIOLET_VERTICAL_BRAND_LINE_PATH = BRAND_LINE_BASE_PATH / 'border_fiolet.jpg'
# Горизонтальные бренд-линии
GREEN_HORISONTAL_BRAND_LINE_PATH = BRAND_LINE_BASE_PATH / 'border_green_horizontal.jpg'
FIOLET_HORISONTAL_BRAND_LINE_PATH = BRAND_LINE_BASE_PATH / 'border_fiolet_horizontal.jpg'
# Папка с изображениями эмоджи
EMOJI_IMAGE_DIR = BASE_PATH_TO_ASSETS / 'emoji/'
# Папка со шрифтами
FONTS_DIR = BASE_PATH_TO_ASSETS / 'fonts/'

# Логотипы
LOGO_PATH = BASE_PATH_TO_ASSETS / 'logo/'
# Изображения с подпишись
SUBSCRIBE_IMAGE_PATH = BASE_PATH_TO_ASSETS / 'subscribe/'
SUBSCRIBE_GREEN_VERTICAL_IMAGE_PATH = (
        SUBSCRIBE_IMAGE_PATH
        / 'green_vertical_subscribe_to_social_network.jpg/'
)
SUBSCRIBE_ORANGE_VERTICAL_IMAGE_PATH = (
        SUBSCRIBE_IMAGE_PATH
        / 'orange_vertical_subscribe_to_social_network.jpg/'
)
