""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """
from pprint import pprint

# from pprint import pprint

from load_data.load_data_from_table import ExcelManager
from load_data.utils.utils import extract_text


def main():
    """
    Главный метод, в котором формируется итоговый словарь с данными пользователя

    {
        'Пол': 'женский',
        'Возраст': 30,
        'Тип волос': 'Тип и описание в виде строки',
        'Тип кожи головы': 'Тип и описание в виде строки',
        'Проблема': 'Тип и описание в виде строки',
        'Пожелания': 'Тип и описание в виде строки,
    }

    :return: словарь c лаконичным описанием параметров
    """

    instance_excel = ExcelManager(file_path='../00_base/00_Средства.xlsx')

    # формирую словари с данными
    dict_with_type_hair = instance_excel.load_hair_type_data(ws_title='Типы волос')
    dict_with_head_skin = instance_excel.load_head_skin_data(ws_title='Типы кожи головы')
    dict_with_problem = instance_excel.load_problems_data(ws_title='Проблемы')
    dict_with_wishes = instance_excel.load_wishes_data(ws_title='Потребности')
    dict_with_product = instance_excel.load_info_about_products(ws_title='Средства')

    # загружаем информацию по пользователю
    dict_with_info_about_user = instance_excel.load_info_about_user(ws_title='Подборки')

    # заполняем данные пользователя значениями из словарей

    final_user_data = {
        'Пол': dict_with_info_about_user['Пол'],
        'Возраст': dict_with_info_about_user['Возраст'],
        'Тип волос': extract_text(
            dict_with_type_hair[dict_with_info_about_user['Тип волос']],
            'Тип',
        ),
        'Тип кожи головы': extract_text(
            dict_with_head_skin[dict_with_info_about_user['Тип кожи головы']],
            'Тип',
        ),
        'Проблема': extract_text(
            dict_with_problem[dict_with_info_about_user['Проблема']],
            'Проблема',
        ),
        'Пожелания': extract_text(
            dict_with_wishes[dict_with_info_about_user['Пожелания']],
            'Потребность',
        ),
    }

    # Формирование общего словаря
    # pprint({
    #     "Пользователь": final_user_data,
    #     "Средства": dict_with_product["Средства"],
    # }, sort_dicts=False)

    return {
        "Пользователь": final_user_data,
        "Средства": dict_with_product["Средства"],
    }


if __name__ == '__main__':
    main()
