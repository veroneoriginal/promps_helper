"""
В этом модуде управляющая функция для реализации процесса отправки запроса в openai,
получение результата и сохранение итогового файла
"""

from appeal_to_openai.utils import (
    _formation_context,
    _generate_text_content_openai,
    _save, _processing_content_from_openai,
)


def main(
        prompt: str,
        system_prompt: str,
        api_key: str,
        folder_name: str = 'prompt/history_prompt',
) -> None:
    """
    Уравляющая функция для реализации процесса отправки запроса в openai,
    получение результата и сохранение итогового файла

    :param api_key: ключ для отправки запроса
    :param folder_name: папка, в которую будет сохраняться ответ openai
    :param prompt: сформированный промпт для отправки запроса
    :param system_prompt: системный промпт для отправки запроса
    :return: None
    """

    # print('Формирование контекста')
    context = _formation_context(
        prompt=prompt,
        system_prompt=system_prompt,
    )

    # print('Передаю контекст в OpenAI.')
    result = _generate_text_content_openai(
        api_key=api_key,
        context=context,
        model="gpt-4o",
    )

    # print('Обрабатываю контент полученный от OpenAI')
    data = _processing_content_from_openai(result=result)


    print('Сохраняю ответ, полученный от OpenAI')
    _save(
        data=data,
        folder_name=folder_name,
    )
