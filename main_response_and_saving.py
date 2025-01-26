# import os
# from datetime import datetime
#
# from openai.openai_func import generate_text_content_openai
# from openai.formation_context import ContextFormation
# from prompt_constructor.settings_constructor.settings_response import settings_response
# from prompt_constructor.settings_constructor.system_prompt import system_prompt
#
#
# load_dotenv()
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#
# context = ContextFormation()
# final_context = context.formation_context(
#     data=data,
#     settings_response=settings_response,
#     system_prompt=system_prompt,
# )
#
# def response_and_save():
#     print('Начинаю процесс')
#     result = generate_text_content_openai(
#         api_key=OPENAI_API_KEY,
#         context=final_context,
#         model="gpt-4o",
#     )
#
#     # вычленяю нужное
#     content = result.choices[0].message.content
#     print(content)
#
#
#     # сохраняю в папку history_prompt
#     # Получение текущей даты и времени
#     current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     folder_name = 'prompt/history_prompt'
#
#     # Убедиться, что папка существует, иначе создать её
#     os.makedirs(folder_name, exist_ok=True)
#
#     # Формирование имени файла
#     file_name = f"Новый запрос_{current_date}.md"
#     file_path = os.path.join(folder_name, file_name)
#        # Сохранение текста в файл
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(content)
#
#     print(f"Файл успешно сохранен: {file_path}")
#
#
# for _ in range(5):
#     response_and_save()
