from typing import Literal

from openai import OpenAI
from openai.types.chat import ChatCompletion


def generate_text_content_openai(
        api_key: str,
        context: list,
        model: Literal["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
) -> ChatCompletion:
    """
    Отправляем запрос на генерацию тестового контента в OpenAI.

    context: контекст от пользователя
    settings: настройки для запроса
    """

    client = OpenAI(api_key=api_key)

    return client.chat.completions.create(
        model=model,
        messages=context,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
