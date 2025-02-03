"""
В этом модуле забираем данные с 2х листов
и формируем единый словарь для создания из него картинки
"""

from pprint import pprint
from excel_process_data.process_data import ExcelManager

instance_excel = ExcelManager(file_path='00_base/00_Средства.xlsx', )
# формирование словаря из Подборок
first_dict = instance_excel.forming_dict_from_collection(ws_title='Подборки')
# дополнение словаря информацией из Средства
second_dict = instance_excel.add_data_from_the_tools_page(
    ws_title="Средства",
    data=first_dict,
)

def creating_dict_for_pdf():
    # теперь из полного словаря создаем словарь, нужный для заполнения данных в pdf
    # {
    # Название : описание,
    # Плюсы : описание,
    # Минусы : описание,
    # Количество меры (число) : описание,
    # Юниты меры (мл/шт): описание,
    # Стоимость руб: описание,
    # Ссылка на изображение в базе: описание,
    # }

    picture_dict = {}

    # Дополнительные ключи, которые мы хотим взять из дополнительной информации
    additional_keys = [
        "Количество меры (число)",
        "Юниты меры (мл/шт)",
        "Стоимость руб",
        "Ссылка на изображение в базе",
    ]

    for product_name, info in second_dict.items():

        # Пропускаем ключ, если он не относится к конкретному средству
        if product_name == "итоговая рекомендация":
            continue

        # Формируем новый словарь для средства с нужными ключами
        new_info = {
            "Название": product_name,
            "Плюсы": info.get("плюсы"),
            "Минусы": info.get("минусы")
        }
        # Добавляем дополнительные данные
        for key in additional_keys:
            new_info[key] = info.get(key, "")

        picture_dict[product_name] = new_info

    print("Словарь для картинки:")
    pprint(picture_dict)
