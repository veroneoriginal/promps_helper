"""
В этом модуде управляющая функция для реализации процесса отправки запроса в openai,
получение результата и сохранение итогового файла
"""

from appeal_to_openai.utils import (
    _formation_context,
    _generate_text_content_openai,
    _save,
    _processing_content_from_openai,
)


def main(
        prompt: str,
        system_prompt: str,
        api_key: str,
        json_scheme: dict,
        folder_name: str,
) -> str:
    """
    Уравляющая функция для реализации процесса отправки запроса в openai,
    получение результата и сохранение итогового файла

    :param prompt: сформированный промпт для отправки запроса
    :param system_prompt: системный промпт для отправки запроса
    :param api_key: ключ для отправки запроса
    :param json_scheme: json_scheme запроса (определяется в зависимости
     от количества анализируемых средств)
    :param folder_name: папка, в которую будет сохраняться ответ openai

    :return: путь до json файла с анализом средств
    """

    # Формирование контекста
    context = _formation_context(
        prompt=prompt,
        system_prompt=system_prompt,
    )

    # Передаю контекст в OpenAI
    result = _generate_text_content_openai(
        api_key=api_key,
        context=context,
        model="gpt-4o",
        json_scheme=json_scheme,
    )

    # Обрабатываю контент полученный от OpenAI
    data = _processing_content_from_openai(result=result)

    # Сохраняю ответ, полученный от OpenAI
    file_path_to_saving_json = _save(
        data=data,
        folder_name=folder_name,
    )

    return file_path_to_saving_json
