""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """

# from pprint import pprint

from load_data.load_data_from_table import ExcelManager

from load_data.formation_single_dict import (
    load_data_table,
    create_final_dict,
)



def main():
    """
    Главный метод, в котором формируется итоговый словарь с данными пользователя

    data = {
        'Пользователь': {
            "Пол": "содержимое ячейки",
            "Возраст": "содержимое ячейки",
            "Тип волос": "содержимое ячейки",
            "Тип кожи головы": "содержимое ячейки",
            "Проблемы": "содержимое ячейки",
            "Пожелания": "содержимое ячейки",
        },

        "Средства": {
            1: {
                "Название": "содержимое ячейки",
                "Состав": "содержимое ячейки",
            },
        },
    }
    :return: словарь c лаконичным описанием параметров
    """

    instance_excel = ExcelManager(file_path='../00_base/00_Средства.xlsx')
    result = load_data_table(instance_excel=instance_excel)
    # pprint(result, sort_dicts=False)

    print(create_final_dict(data=result))

    return create_final_dict(data=result)

    # final_user_data = {
    #     'Пол': dict_with_info_about_user['Пол'],
    #     'Возраст': dict_with_info_about_user['Возраст'],
    #     'Тип волос': extract_text(
    #         dict_with_type_hair[dict_with_info_about_user['Тип волос']],
    #         'Тип',
    #     ),
    #     'Тип кожи головы': extract_text(
    #         dict_with_head_skin[dict_with_info_about_user['Тип кожи головы']],
    #         'Тип',
    #     ),
    #     'Проблема': extract_text(
    #         dict_with_problem[dict_with_info_about_user['Проблема']],
    #         'Проблема',
    #     ),
    #     'Пожелания': extract_text(
    #         dict_with_wishes[dict_with_info_about_user['Пожелания']],
    #         'Потребность',
    #     ),
    # }

    # # Формирование общего словаря
    # # pprint({
    # #     "Пользователь": final_user_data,
    # #     "Средства": dict_with_product["Средства"],
    # # }, sort_dicts=False)
    #
    # return {
    #     "Пользователь": final_user_data,
    #     "Средства": dict_with_product["Средства"],
    # }


if __name__ == '__main__':
    main()
