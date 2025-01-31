""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """

# from pprint import pprint

from load_data.load_data_from_table import ExcelManager

from load_data.formation_single_dict import (
    load_data_table,
    create_final_dict,
)


def main():
    """
    Главный метод, в котором вызываются функции по работе с формированием данных с листов excel

    :return: словарь c лаконичным описанием параметров
    """

    instance_excel = ExcelManager(file_path='../00_base/00_Средства.xlsx')
    result = load_data_table(instance_excel=instance_excel)

    # pprint(create_final_dict(data=result))

    return create_final_dict(data=result)


if __name__ == '__main__':
    main()
