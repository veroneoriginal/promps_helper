""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """
from pprint import pprint

from load_data.load_data_from_table import ExcelManager


def main():
    """ Главный метод, в котором формируется итоговый список с данными пользователя """

    instance_excel = ExcelManager(file_path='../00_base/00_Средства.xlsx')

    # формирую словари с данными
    dict_with_type_hair = instance_excel.load_hair_type_data(ws_title='Типы волос')
    pprint(dict_with_type_hair, sort_dicts=False)

    dict_with_head_skin = instance_excel.load_head_skin_data(ws_title='Типы кожи головы')
    pprint(dict_with_head_skin, sort_dicts=False)

    dict_with_problem = instance_excel.load_problems_data(ws_title='Проблемы')
    pprint(dict_with_problem, sort_dicts=False)

    dict_with_wishes = instance_excel.load_wishes_data(ws_title='Потребности')
    pprint(dict_with_wishes, sort_dicts=False)

    # загружаем информацию по пользователю
    dict_with_info_about_user = instance_excel.load_info_about_user(ws_title='Подборки')
    pprint(dict_with_info_about_user, sort_dicts=False)

    # заполняем данные пользователя
    # и вот здесь я должна заполнить значениями из словарей
    # {
    #     'Пол': 'женский',
    #     'Возраст': 30,
    #     'Тип волос': '2, 4',
    #     'Тип кожи головы': 1,
    #     'Проблема': 2,
    #     'Пожелания': 1,
    # }


if __name__ == '__main__':
    main()
