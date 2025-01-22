import os
import time

from datetime import datetime
import asyncio
import aiofiles
from dotenv import load_dotenv
from prompt.openai_func import generate_text_content_openai
from prompt.prompts_2 import context

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
folder_name = 'history_prompt'


async def response_and_save():
    print('Начинаю процесс')

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        generate_text_content_openai,
        OPENAI_API_KEY,
        context,
        "gpt-4o"
    )

    # result = generate_text_content_openai(
    #     api_key=OPENAI_API_KEY,
    #     context=context,
    #     model="gpt-4o",
    # )

    # Добавляем задержку для предотвращения превышения лимита запросов
    # await asyncio.sleep(5)

    # вычленяю нужное
    content = result.choices[0].message.content
    print(content)

    # Получение текущей даты и времени
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Формирование имени файла
    file_name = f"{current_date}.md"
    file_path = os.path.join(folder_name, file_name)

    # Асинхронное сохранение текста
    async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
        await file.write(content)

    print(f"Файл успешно сохранен: {file_path}")


# Основная корутина для запуска нескольких вызовов
async def main():
    tasks = [response_and_save() for _ in range(10)]  # 10 вызовов
    time.sleep(5)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
