from typing import Any

from prompt_constructor.json_schemes.js_for_one_product import create_json_scheme_for_one_product

FIELD_TITLES = {
    "main_components": "Основные компоненты",
    "active_ingredients": "Активные ингредиенты",
    "moisturizing_and_care": "Увлажняющие и ухаживающие компоненты",
    "preservatives_and_ph_regulators": "Консерванты и регуляторы pH",
    "banned_or_unwanted": "Запрещенные или нежелательные компоненты",
    "additional_properties": "Дополнительные свойства",
    "texture": "Текстура",
    "plus": "Плюсы",
    "minus": "Минусы",
    "conclusion": "Вывод",

    # Расширенные поля из категорий
    "skin_type_impact": "Влияние на тип кожи",
    "exfoliation_intensity": "Интенсивность пилинга",
    "protection_duration": "Длительность защиты",
    "foaming_effect": "Пенообразование",
    "spf_level": "Уровень SPF",
    "application_time": "Время нанесения",
    "ph_level": "Уровень pH",
    "eye_area_effect": "Эффект на область глаз",
    "durability": "Стойкость",
    "finish": "Финиш",
    "pigmentation": "Пигментация",
    "coverage": "Покрытие",
    "water_resistance": "Водостойкость",
    "fixation_level": "Степень фиксации",
    "hair_feel": "Ощущение на волосах",
    "main_notes": "Основные ноты",
    "scent_evolution": "Раскрытие аромата",
}


def forming_info_for_pdf_best_product(
        data: dict,
) -> list:
    """
    Функция для формирования списка словарей, которые нужны для наполнения картинки
    для кодов 'Лучшее средство' и 'Лучшее средство без канцерогенов'

    :param data: словарь со всей информацией по средствам для текущей подборки
    :return: список словарей с информацией для вставки в изображение
     [
    {'Название': 'YVES ROCHER Volume Plumping Shampoo Sulfate Free',
    'Плюсы': 'Содержит экстракт киноа и инулин, которые могут укреплять и '
           'увлажнять волосы. Без сульфатов, что делает его мягким для волос.',
    'Минусы': 'Основной акцент на объем, а не на увлажнение, что может быть '
            'недостаточно для сухих волос.',
    'Соотношение': '300''мл'/ 750 руб.,
    'Ссылка на изображение в базе': '00_base/products/00_img/yves_free.jpg',
    'Лучшее средство': False,
    ]
    """

    # создаем список
    list_for_pdf = []

    # формируем список из словарей по средствам, которые надо преобразовать в картинку
    for name_product, info in data.items():
        ratio = (f'{info.get("Количество меры (число)")} '
                 f'{info.get("Юниты меры (мл/шт)")} / {info.get("Стоимость руб")} рублей')

        list_for_pdf.append(
            {
                "Название": name_product,
                "Плюсы": info["plus"],
                "Минусы": info["minus"],
                "Соотношение": ratio,
                "Ссылка на изображение в базе": info.get("Ссылка на изображение в базе"),
                "Лучшее средство": info["best_product"],
            }
        )

    return list_for_pdf


# def forming_info_for_pdf_one_product(
#         data: dict,
# ) -> dict[str | Any, Any] | None:
#     """
#     Функция для формирования списка словарей, которые
#     нужны для наполнения картинки для кода 'Разбор состава одного средства'
#
#     :return: словарь с ключами для отображения для на pdf для одного средства
#     """
#
#     # формируем список из словарей по средствам, которые надо преобразовать в картинку
#     for name_product, info in data.items():
#         ratio = (f'{info.get("Количество меры (число)")} '
#                  f'{info.get("Юниты меры (мл/шт)")} / {info.get("Стоимость руб")} рублей')
#
#         return {
#             "Название": name_product,
#             "Основные компоненты": info["main_components"],
#             "Активные ингредиенты": info["active_ingredients"],
#             "Увлажняющие и ухаживающие компоненты": info["moisturizing_and_care"],
#             "Консерванты и регуляторы pH": info["preservatives_and_ph_regulators"],
#             "Запрещенные или нежелательные компоненты": info["banned_or_unwanted"],
#             "Дополнительные свойства": info["additional_properties"],
#             "Текстура": info["texture"],
#             "Плюсы": info["plus"],
#             "Минусы": info["minus"],
#             "Вывод": info["conclusion"],
#             "Соотношение": ratio,
#             "Ссылка на изображение в базе": info.get("Ссылка на изображение в базе"),
#
#         }


def forming_info_for_pdf_one_product(
        data: dict,
        data_task: dict,
) -> dict[str | Any, Any] | None:
    """
    Функция для формирования списка словарей, которые
    нужны для наполнения картинки для кода 'Разбор состава одного средства'

    :param data: словарь со средством, его плюсами, минусами и другими параметрами
    :param data_task: словарь с кодом задачи, количеством средств, категорией продукта
    :return: словарь с ключами для отображения для на pdf для одного средства
    """
    for name_product, info in data.items():
        # Получаем категорию из задачи
        category = data_task.get("Категория", "")

        # Получаем JSON-схему под эту категорию
        schema = create_json_scheme_for_one_product({"Категория": category})

        # Берем все ключи из product -> properties
        product_properties = schema["schema"]["properties"]["product"]["properties"]

        # Базовые данные, которые идут всегда
        pdf_data = {
            "Название": name_product,
            "Соотношение": (
                f'{info.get("Количество меры (число)", "")} '
                f'{info.get("Юниты меры (мл/шт)", "")} / {info.get("Стоимость руб", "")} рублей'
            ),
            "Ссылка на изображение в базе": info.get("Ссылка на изображение в базе", ""),
        }

        # Добавляем все поля по маппингу FIELD_TITLES
        for field_key in product_properties:
            title = FIELD_TITLES.get(field_key, field_key)  # Берем красивое название или ключ
            pdf_data[title] = info.get(field_key, "")

        return pdf_data  # Возвращаем сразу, потому что продуктов у нас один


def main_forming_info_for_pdf(
        data: dict,
        data_task: dict,
) -> list:
    """
    Главная функция, которая определяет какая схема построения pdf-файла
    будет формироваться для текущей подборки

    :param data: словарь со средствами, их плюсами, минусами и прочим
    :param data_task: словарь с кодом задачи, количеством средств, категорией продукта

    :return: список словарей с информацией для вставки в изображение
    """

    forming = {
        'Лучшее средство': forming_info_for_pdf_best_product,
        'Лучшее средство без канцерогенов': forming_info_for_pdf_best_product,
        'Разбор состава одного средства': forming_info_for_pdf_one_product,
    }

    task = data_task["Задача"]

    if task == 'Разбор состава одного средства':
        result = forming_info_for_pdf_one_product(data=data, data_task=data_task)
    else:
        result = forming[task](data)

    return result
