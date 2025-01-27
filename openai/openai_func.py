""" В этом модуле реализована логика отправки запроса на генерацию тестового контента в OpenAI."""

from typing import Literal

import openai


def generate_text_content_openai(
        api_key: str,
        context: list,
        model: Literal["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
):
    """
    Отправляем запрос на генерацию тестового контента в OpenAI.

    context: ранее сформированный контекст запроса
    """

    # Устанавливаем ключ API
    openai.api_key = api_key

    return openai.ChatCompletion.create(
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
