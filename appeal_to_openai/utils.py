"""
В этом модуде функции, с помощью которых реализован процесс отправки запроса в openai,
получение результата и сохранение итогового файла
"""

import os
import re
import json
from pathlib import Path
from typing import Literal, Optional, Any
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
        model: Literal["gpt-4o", "gpt-4o-mini",],
        json_scheme: dict,
) -> ChatCompletion:
    """
    Функция для отправки запроса на генерацию тестового контента в OpenAI.

    :param api_key: ключ для подключения к OpenAI,
    :param context: сформированный контекст запроса,
    :param model: название используемой модели OpenAI
    :param json_scheme: json_scheme запроса (определяется в зависимости
     от количества анализируемых средств)

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
            "type": "json_schema",
            "json_schema": json_scheme,
        }
    )


def _processing_content_from_openai(
        result: ChatCompletion,
) -> Optional[Any] | None:
    """
    Функция для обработки контента из ответа от OpenAI

    :param result: ответ от OpenAI
    :return: контент в json или None
    """

    # вычленяю нужное из ответа OpenAi
    content = result.choices[0].message.content

    # очищаю контент, чтобы был очищенный json
    cleaned_response = re.sub(r'```json|```', '', content).strip()

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка в JSON перед сохранением: {e}")
        return None


def _save(
        data: Optional[Any],
        folder_name: str,
        json_filename: str = "Анализ_средств.json"
) -> str:
    """
    Функция для сохранения ответа, полученного от OpenAI

    :param data: обработанный контент от OpenAI
    :param folder_name: путь, куда сохранять ответ от OpenAI
    :return: путь до файла json файла с анализом средств
    """

    # Формирование имени файла
    file_path = os.path.join(folder_name, json_filename)

    # Сохранение текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # print(f"Файл успешно сохранен: {file_path}")
    return file_path


def checking_file_with_response(
        json_file_path: str,
) -> Optional[Any] | None:
    """
    Функция для открытия файла с ответом OpenAI и проверки,
    что формат файла с ответом соответствует заданному.

    :param json_file_path: путь до файла с ответом OpenAI
    :return: JSON-данные или None
    """

    json_file_path = Path(json_file_path) / 'Анализ_средств.json'

    with open(json_file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)

        except json.JSONDecodeError as e:
            print(f"❌ Ошибка в JSON: {e}")
            return None
