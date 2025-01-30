""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """
from pprint import pprint

from load_data.load_data_from_table import ExcelManager

if __name__ == '__main__':
    instance_excel = ExcelManager(file_path='../00_base/00_Средства.xlsx')
    dict_with_info = instance_excel.load_hair_type_data(ws_title='Типы волос')
    pprint(dict_with_info)
