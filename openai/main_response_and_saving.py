"""
В этом модуде отправка запроса в openai и сохранение итогового файла
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from openai.openai_func import generate_text_content_openai


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def response_and_save(
        context: list
):
    print('Передаю контекст в generate_text_content_openai.')
    result = generate_text_content_openai(
        api_key=OPENAI_API_KEY,
        context=context,
        model="gpt-4o",
    )

    # вычленяю нужное
    content = result.choices[0].message.content

    # сохраняю в папку history_prompt
    # Получение текущей даты и времени
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = 'prompt/history_prompt'

    # Убедиться, что папка существует, иначе создать её
    os.makedirs(folder_name, exist_ok=True)

    # Формирование имени файла
    file_name = f"Новый запрос_{current_date}.md"
    file_path = os.path.join(folder_name, file_name)
    # Сохранение текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Файл успешно сохранен: {file_path}")
