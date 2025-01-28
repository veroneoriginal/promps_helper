"""
В этом модуле идет формирование контекста
"""


def formation_context(
        prompt,
        system_prompt,
):
    """Функция для формирования контекста"""

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

    return context
