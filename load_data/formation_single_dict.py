# from pprint import pprint

from load_data.utils.utils import extract_text


def load_data_table(instance_excel) -> dict:
    """
    Функция для создания общего словаря из листов Excel

    :param instance_excel: объект класса ExcelManager, работающий с таблицей
    :return: словарь с загруженными данными
    """

    return {
        "Типы волос": instance_excel.load_hair_type_data(ws_title='Типы волос'),
        "Типы кожи головы": instance_excel.load_head_skin_data(ws_title='Типы кожи головы'),
        "Проблемы": instance_excel.load_problems_data(ws_title='Проблемы'),
        "Потребности": instance_excel.load_wishes_data(ws_title='Потребности'),
        "Средства": instance_excel.load_info_about_products(ws_title='Средства'),
        "Пользователь": instance_excel.load_info_about_user(ws_title='Подборки'),
    }



def create_final_dict(data: dict) -> dict:


    final_user_data = {
        'Пол': data['Пользователь']['Пол'],
        'Возраст': data['Пользователь']['Возраст'],
        'Тип волос': extract_text(data['Типы волос'][data['Пользователь']['Тип волос']], 'Тип', )

        #     dict_with_type_hair[dict_with_info_about_user['Тип волос']],
        #     'Тип',
        # ),
        # 'Тип кожи головы': extract_text(
        #     dict_with_head_skin[dict_with_info_about_user['Тип кожи головы']],
        #     'Тип',
        # ),
        # 'Проблема': extract_text(
        #     dict_with_problem[dict_with_info_about_user['Проблема']],
        #     'Проблема',
        # ),
        # 'Пожелания': extract_text(
        #     dict_with_wishes[dict_with_info_about_user['Пожелания']],
        #     'Потребность',
        # ),
    }
    return final_user_data


    # Формирование общего словаря
    # pprint({
    #     "Пользователь": final_user_data,
    #     "Средства": dict_with_product["Средства"],
    # }, sort_dicts=False)
