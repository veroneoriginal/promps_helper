"""
В этом модуле работа всей логики по забору данных с 2х листов,
и формирование единого словаря для помещения информации в картинку
"""

import os

from info_for_picture.step_1 import forming_dict_from_collection
from info_for_picture.step_2 import add_data_from_the_tools_page
from info_for_picture.step_3 import creating_dict_for_pdf



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "00_base", "00_Средства.xlsx")

# формирование словаря из Подборок
first_dict = forming_dict_from_collection(
    file_path=file_path,
    ws_title='Подборки'
)
print('Шаг 1 сделан')

# дополнение словаря информацией из Средства
second_dict = add_data_from_the_tools_page(
    ws_title="Средства",
    file_path=file_path,
    data=first_dict,
)
print('Шаг 2 сделан')

creating_dict_for_pdf(dict_full_info=second_dict)
print('Шаг 3 сделан')
