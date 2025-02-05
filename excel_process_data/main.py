""" В этом модуле реализована логика вызовов функций для загрузки данных из таблиц """


from excel_process_data.process_data import ExcelManager

from excel_process_data.formation_single_dict import (
    load_data_table,
    create_final_dict,
)


def main(
        file_path: str,
) -> dict:
    """
    Главный метод, в котором вызываются функции по работе с формированием данных с листов excel

    :param file_path: путь до документа .xlsx
    :return: словарь c лаконичным описанием параметров
    """

    instance_excel = ExcelManager(file_path=file_path)

    result = load_data_table(instance_excel=instance_excel)

    return create_final_dict(data=result)


if __name__ == '__main__':
    main(file_path='../00_base/00_Средства.xlsx')
