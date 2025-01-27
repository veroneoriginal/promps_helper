"""
В этом модуде вызов ключевых функций - от забора данных из таблицы до отправки в openai
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from openai.formation_context import formation_context
from openai.openai_func import generate_text_content_openai
from prompt_constructor.constructor import PromptConstructor
from prompt_constructor.settings_constructor.settings_response import SETTINGS_RESPONSE
from prompt_constructor.settings_constructor.system_prompt import SYSTEM_PROMPT

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



def create_context_for_request_to_openai():
    """
    В этой функции собраны все этапы с момента забора информации из таблицы
    до создания готового контекста, который передается в OpenAI
    """

    print('Забираю данные для анализа из таблицы.')
    # скрипт проходит по таблице, и забирает данные из ячеек, формируя словарь ключ-значение,
    # где ключ это название столбца, а значение - содержимое ячейки
    # словарь будет иметь вид
    data_with_info_about_user_and_product = {
        'Пользователь': {
            "Пол": "содержимое ячейки",
            "Возраст": "содержимое ячейки",
            "Тип волос": "содержимое ячейки",
            "Тип кожи головы": "содержимое ячейки",
            "Особенности": "содержимое ячейки",
            "Проблемы или пожелания": "содержимое ячейки",
        },

        "Средства": {
            1: {
                "Название": "содержимое ячейки",
                "Состав": "содержимое ячейки",
            },
            2: {
                "Название": "содержимое ячейки",
                "Состав": "содержимое ячейки",
            },
            3: {
                "Название": "содержимое ячейки",
                "Состав": "содержимое ячейки",
            }
        },
    }

    print('Собираю промпт.')
    instance_create_prompt = PromptConstructor()
    prompt = instance_create_prompt.construct_prompt(
        data=data_with_info_about_user_and_product,
        settings_response=SETTINGS_RESPONSE,
    )

    print('Передаю промпт в контекст.')
    context = formation_context(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )

    return context


def response_and_save():
    print('Начинаю процесс')
    context = create_context_for_request_to_openai()

    print('Передаю контекст в generate_text_content_openai.')
    result = generate_text_content_openai(
        api_key=OPENAI_API_KEY,
        context=context,
        model="gpt-4o",
    )

    # вычленяю нужное
    content = result.choices[0].message.content
    print(content)

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


for _ in range(5):
    response_and_save()
