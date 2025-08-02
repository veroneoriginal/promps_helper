# pylint: skip-file

"""
При запуске модуля:
1) в файл "dev_helpers/data.json" записывается весь словарь со всеми данными из
книги '00_base/Средства.xlsx'
2) из модуля "dev_helpers/data_tools_for_test" можно забирать в тесты ALL_DATA_TOOLS_FOR_TEST
НЕ ЗАБУДЬ сначала спарсить средства, чтобы были изображения
"""

from dev_helpers.get_data_tools import get_data_tools_for_test
import requests
import os

from source.structure_folders import EMOJI_IMAGE_DIR


def download_smiles():
    """
    Скачивает изображения смайликов в библиотеку emojipy
    """

    twemoji_emoji = {
        '26a0': 'warning',  # ⚠
        '1f9d1': 'person',  # 🧑
        '1f469': 'woman',  # 👩
        '1f646': 'person_gesturing_ok',  # 🙆
        '1f486': 'person_getting_massage',  # 💆
        '1f60a': 'smiling_face',  # 😊
        '2705': 'white_check_mark',
        '274c': 'x',
        '1f602': 'joy',
        '1f603': 'smiley',
        '1f604': 'smile',
        '1f44d': 'thumbs_up',
        '1f525': 'fire',
        '1f389': 'party_popper',
        '1f60d': 'heart_eyes',
        '1f622': 'cry',
        '1f44f': 'clap',
        '2764': 'heart',
        '1f64f': 'pray',
        '1f62d': 'sob',
        '1f64c': 'raised_hands',
        '1f913': 'nerd_face',
        '1f92f': 'exploding_head',
        '1f631': 'scream',
        '1f60e': 'sunglasses',
        '1f4cc': 'pushpin',
        '1f382': 'birthday_cake',  # 🎂
        '1f539': 'small_blue_diamond',  # 🔹
        '1f50d': 'magnifying_glass',  # 🔍
        '2b50': 'star',  # ⭐
        '1f3c6': 'trophy',  # 🏆
        '1f484': 'lipstick',  # 💄
    }

    output_dir = EMOJI_IMAGE_DIR
    os.makedirs(output_dir, exist_ok=True)

    base_url = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/'

    for code, name in twemoji_emoji.items():
        filename = f'{code}.png'
        url = base_url + filename
        filepath = os.path.join(output_dir, filename)

        print(f'⬇️  Downloading {name} → {filepath}')
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f'✅ Saved: {filename}')
        except Exception as e:
            print(f'❌ Failed to download {filename}: {e}')


if __name__ == "__main__":
    # get_data_tools_for_test()
    download_smiles()
