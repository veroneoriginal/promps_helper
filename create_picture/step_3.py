from openpyxl import load_workbook
from create_picture.step_2 import main_step_two

from pprint import pprint

result = main_step_two()

# теперь из имеющегося словаря создаем словарь, нужный для картинки

# Название
# Плюсы
# Минусы
# Количество меры (число)
# Юниты меры (мл/шт)
# Стоимость руб


picture_dict = {}

# Дополнительные ключи, которые мы хотим взять из дополнительной информации
additional_keys = ["Количество меры (число)", "Юниты меры (мл/шт)", "Стоимость руб"]

for product_name, info in result.items():
    print(product_name)
    # print( info)

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