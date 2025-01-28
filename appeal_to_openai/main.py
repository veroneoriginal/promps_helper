"""
В этом модуде управляющая функция для реализации процесса отправки запроса в openai,
получение результата и сохранение итогового файла
"""
import os
from dotenv import load_dotenv
from appeal_to_openai.utils import (
    formation_context,
    generate_text_content_openai,
    save,
)


def main(
        prompt: str,
        system_prompt: str,
) -> None:
    """
    Уравляющая функция для реализации процесса отправки запроса в openai,
    получение результата и сохранение итогового файла

    :param prompt: сформированный промпт для отправки запроса
    :param system_prompt: системный промпт для отправки запроса
    """

    print('Формирование контекста')
    context = formation_context(
        prompt=prompt,
        system_prompt=system_prompt,
    )

    print('Передаю контекст в OpenAI.')
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    result = generate_text_content_openai(
        api_key=openai_api_key,
        context=context,
        model="gpt-4o",
    )

    print('Сохраняю ответ, полученный от OpenAI')
    save(result=result)
