"""
В этом модуде функции, с помощью которых реализован процесс отправки запроса в openai,
получение результата и сохранение итогового файла
"""

import os
import re
import json
# from datetime import datetime
from typing import Literal
from openai import OpenAI
from openai.types.chat import ChatCompletion

def _formation_context(
        prompt: str,
        system_prompt: str,
) -> list:
    """
    Функция для формирования контекста

    :param prompt: сформированный промпт для отправки запроса
    :param system_prompt: системный промпт для отправки запроса
    :return: подготовленный список для отправки запроса
    """

    return [
        {'role': 'system',
         'content': [
             {
                 'type': 'text',
                 'text': system_prompt,
             }
         ]
         },

        {'role': 'user',
         'content': [
             {
                 'type': 'text',
                 'text': prompt,
             }
         ]
         }
    ]


def _generate_text_content_openai(
        api_key: str,
        context: list,
        model: Literal["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
) -> ChatCompletion:
    """
    Функция для отправки запроса на генерацию тестового контента в OpenAI.

    :param api_key: ключ для подключения к OpenAI,
    :param context: сформированный контекст запроса,
    :param model: название используемой модели OpenAI

    :return: объект ChatCompletion
    """

    # Устанавливаем ключ API

    client = OpenAI(api_key=api_key)

    return client.chat.completions.create(
        model=model,
        messages=context,
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )


def _save(
        result: ChatCompletion,
        folder_name: str,
) -> None:
    """
    Функция для сохранения ответа, полученного от OpenAI

    :param result: ответ от OpenAI
    :param folder_name: путь, куда сохранять ответ от OpenAI
    :return: None
    """

    # вычленяю нужное
    content = result.choices[0].message.content

    # очищаю, чтобы был очищенный json
    cleaned_response = re.sub(r'```json|```', '', content).strip()

    try:
        data = json.loads(cleaned_response)
        # print("✅ JSON корректный!")
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка в JSON перед сохранением: {e}")
        return  # Не сохраняем файл, если JSON сломан

    # Убедиться, что папка prompt/history_prompt существует, иначе создать её
    os.makedirs(folder_name, exist_ok=True)

    # Формирование имени файла
    file_name = "Анализ_средств.json"
    file_path = os.path.join(folder_name, file_name)

    # Сохранение текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Файл успешно сохранен: {file_path}")
