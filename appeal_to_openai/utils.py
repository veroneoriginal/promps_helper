"""
В этом модуде функции, с помощью которых реализован процесс отправки запроса в openai,
получение результата и сохранение итогового файла
"""

import re
import json
from decimal import Decimal, ROUND_UP
from pathlib import Path
from typing import (
    Optional,
    Any,
)
from openai import OpenAI
from openai.types.chat import ChatCompletion

PER_TOKEN_COUNT = 1_000_000

TOKEN_PRICE = {
    'usd_price_in_rub': 100,
    'gpt-4o-mini': {
        'prompt': 0.15 / PER_TOKEN_COUNT,  # 0.00000015
        'cached_prompt': 0.075 / PER_TOKEN_COUNT,  # 0,000000075
        'completion': 0.60 / PER_TOKEN_COUNT,  # 0.0000006
    },
    'dall-e-3': {
        'one_image': 0.08,
    },
    'gpt-4o': {
        'prompt': 2.50 / PER_TOKEN_COUNT,  # 0.0000025
        'cached_prompt': 1.25 / PER_TOKEN_COUNT,  # 0.00000125
        'completion': 10 / PER_TOKEN_COUNT,  # 0.00001
    },
    'gpt-4.5-preview': {
        'prompt': 75 / PER_TOKEN_COUNT,  # 0,000075
        'cached_prompt': 37.50 / PER_TOKEN_COUNT,  # 0,0000375
        'completion': 150 / PER_TOKEN_COUNT,  # 0,00015
    },
}


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
        model: str,
        json_scheme: dict,
) -> ChatCompletion:
    """
    Функция для отправки запроса на генерацию тестового контента в OpenAI.

    :param api_key: ключ для подключения к OpenAI,
    :param context: сформированный контекст запроса,
    :param model: название используемой модели OpenAI "gpt-4o", "gpt-4o-mini"
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
        tools=[
            {
                "type": "function",
                "function": {
                    "name": json_scheme["name"],
                    "parameters": json_scheme["schema"]
                }
            }
        ],
    )


def _processing_answer_from_openai(
        result: ChatCompletion,
        model: str
) -> Optional[Any] | None:
    """
    Функция для обработки контента из ответа от OpenAI

    :param result: ответ от OpenAI
    :param model: имя модели OpenAI ('gpt-4o', 'gpt-4o-mini')
    :return: словарь с контентом и прайсом на токены
    """

    # получаем контент из ответа OpenAI
    content = get_content(data=result)
    # получаем количество и стоимость потраченных токенов
    token_price = get_token_price(
        data=result,
        model=model,
    )

    return {
        'content': content,
        'token_price': convert_decimals_to_strings(token_price)
    }


def get_token_price(
        data: ChatCompletion,
        model: str
) -> dict | None:
    """
    Получаем словарь с количеством и стоимостью токенов из ответа OpenAI

    :param data: объект ответа OpenAI
    :param model: имя модели OpenAI ('gpt-4o', 'gpt-4o-mini')
    """
    token_price = calc_text_responce_price(
        data=data,
        model=model
    )
    return token_price


def get_content(
        data: ChatCompletion
) -> dict | None:
    """
    Получаем словарь с контентом из ответа OpenAI
    :param data: объект ответа OpenAI
    :return: словарь с контентом ответа
    """
    # получаем контент из ответа OpenAI
    content = data.choices[0].message.tool_calls[0].function.arguments

    # очищаю контент, чтобы был очищенный json
    cleaned_response = re.sub(r'```json|```', '', content).strip()

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка при извлечении JSON из ответа OpenAI перед сохранением: {e}")
        return None


def calc_text_responce_price(
        data: ChatCompletion,
        model: str,
) -> dict:
    """
    Считает стоимость запроса генерации текста по прайсу для
    конкретной модели.
    :param data: объект ответа OpenAI
    :param model: имя модели OpenAI ('gpt-4o', 'gpt-4o-mini')
    :return: словарь с количество и стоимостью токенов
    """
    # Расчёт кешированных токенов промпта
    prompt_cached_token_count = data.usage.prompt_tokens_details.cached_tokens
    prompt_cached_token_usd = (
            to_decimal(prompt_cached_token_count)
            * to_decimal(TOKEN_PRICE[model]['cached_prompt'])
    )
    prompt_cached_token_rub = (
            to_decimal(prompt_cached_token_usd)
            * to_decimal(TOKEN_PRICE['usd_price_in_rub'])
    )
    # Расчёт токенов промпта, исключаем закешированные токены
    prompt_token_count = data.usage.prompt_tokens - prompt_cached_token_count
    prompt_token_usd = (
            to_decimal(prompt_token_count)
            * to_decimal(TOKEN_PRICE[model]['prompt'])
    )
    prompt_token_rub = (
            to_decimal(prompt_token_usd)
            * to_decimal(TOKEN_PRICE['usd_price_in_rub'])
    )
    # Расчёт токенов ответа
    completion_token_count = data.usage.completion_tokens

    completion_token_usd = (
            to_decimal(completion_token_count)
            * to_decimal(TOKEN_PRICE[model]['completion'])
    )
    completion_token_rub = (
            to_decimal(completion_token_usd)
            * to_decimal(TOKEN_PRICE['usd_price_in_rub'])
    )
    # Общий расчёт всех токенов
    total_tokens_count = (
            prompt_token_count + prompt_cached_token_count + completion_token_count
    )
    total_tokens_usd = (
            prompt_token_usd + prompt_cached_token_usd + completion_token_usd
    )
    total_tokens_rub = (
            prompt_token_rub + prompt_cached_token_rub + completion_token_rub
    )

    return {
        'prompt_cached': {
            'count': prompt_cached_token_count,
            'USD': prompt_cached_token_usd,
            'RUB': prompt_cached_token_rub,
        },
        'prompt': {
            'count': prompt_token_count,
            'USD': prompt_token_usd,
            'RUB': prompt_token_rub,
        },

        'completion': {
            'count': completion_token_count,
            'USD': completion_token_usd,
            'RUB': completion_token_rub,
        },
        'total': {
            'count': total_tokens_count,
            'USD': total_tokens_usd,
            'RUB': total_tokens_rub,
        }
    }


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


def to_decimal(price: float | int | str) -> Decimal:
    """
    Приводит стоимость к Decimal с высокой точностью дробной части
    """
    return Decimal(str(price)).quantize(Decimal('0.0000000000000'), rounding=ROUND_UP)


def convert_decimals_to_strings(obj: dict) -> dict:
    """
    В словаре заменяет Decimal на строковое представление
    """
    if isinstance(obj, dict):
        return {k: convert_decimals_to_strings(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return obj.to_eng_string()
    return obj
