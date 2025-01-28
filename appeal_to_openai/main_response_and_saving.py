"""
В этом модуде отправка запроса в openai и сохранение итогового файла
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion
from appeal_to_openai.openai_func import generate_text_content_openai


def get_response(
        context: list,
) -> ChatCompletion:
    """
    Функция для вызова функции отправки запроса в OpenAI

    param: context: сформированный контекст запроса
    """

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    return generate_text_content_openai(
        api_key=openai_api_key,
        context=context,
        model="gpt-4o",
    )


def save(
        result: ChatCompletion,
        folder_name: str = 'prompt/history_prompt',
) -> None:
    """
    Функция для сохранения ответа, полученного от OpenAI

    :param result: ответ от OpenAI
    :param folder_name: путь, куда сохранять ответ от OpenAI
    :return: None
    """

    # вычленяю нужное
    content = result.choices[0].message.content

    # сохраняю в папку history_prompt
    # Получение текущей даты и времени
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Убедиться, что папка существует, иначе создать её
    os.makedirs(folder_name, exist_ok=True)

    # Формирование имени файла
    file_name = f"Новый запрос_{current_date}.md"
    file_path = os.path.join(folder_name, file_name)
    # Сохранение текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Файл успешно сохранен: {file_path}")


if __name__ == "__main__":
    print('Передаю контекст в generate_text_content_openai.')
    list_with_info = []
    answer_gpt = get_response(context=list_with_info)
    save(answer_gpt)
