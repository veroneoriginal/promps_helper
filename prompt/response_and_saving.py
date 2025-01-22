import os
from datetime import datetime
from dotenv import load_dotenv
from prompt.openai_func import generate_text_content_openai
from prompt.prompts_2 import context

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



def response_and_save():
    print('Начинаю процесс')
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
    folder_name = 'history_prompt'

    # Формирование имени файла
    file_name = f"{current_date}.md"
    file_path = os.path.join(folder_name, file_name)
       # Сохранение текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Файл успешно сохранен: {file_path}")


for _ in range(10):
    response_and_save()
