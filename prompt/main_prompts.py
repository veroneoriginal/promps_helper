# from prompt.prompts_1 import (
#     gender,
#     age,
#     type_hair,
#     type_scalp,
#     features,
#     features_or_problem,
#     info_about_cosmetics,
# )

# from prompt.prompts_2 import (
#     gender,
#     age,
#     type_hair,
#     type_scalp,
#     features,
#     features_or_problem,
#     info_about_cosmetics,
# )

from prompt.prompts_3 import (
    gender,
    age,
    type_hair,
    type_scalp,
    features,
    features_or_problem,
    info_about_cosmetics,
)


# from prompt.prompts_4 import (
#     gender,
#     age,
#     type_hair,
#     type_scalp,
#     features,
#     features_or_problem,
#     info_about_cosmetics,
# )

from prompt.wishes import user_request




system_prompt = """
Ты профессиональный трихолог с медицинским образованием.
Твоя задача подобрать максимально подходящее средство для человека. 
Данные человека будут даны. 
Отвечай всегда в Markdown.
"""

prompt = f"""
Человек, для которого надо подобрать средство:
Пол: {gender}, возраст: {age} лет.
Тип волос: {type_hair}
Тип кожи головы: {type_scalp}
Особенности: {features}
Дополнительная информация: {features_or_problem}

Информация о составах средств = {info_about_cosmetics}

Учти всю вышепредставленную информацию и проведи анализ составов.

Ответ ты должен дать в следующем виде: {user_request}

"""

context = [
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
