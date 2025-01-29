""" В этом модуле реализована логика вызова функций для загрузки данных из 2х таблиц """

from load_data.load_data_from_table import (
    _load_info_about_user,
    _load_info_about_products,
)


def main(
        file_path: str,
        ws_title_user: str,
        ws_title_product: str,
) -> dict:
    """
    Главная функция, внутри которой осуществляется:
    1) загрузка данных из таблицы 00_Средства -> лист "Подборки"
    2) загрузка данных из таблицы 00_Средства -> лист "Средства"
    3) формирование общего словаря для дальнейше йработы с данными

    :param file_path: путь до документа xlsx
    :param ws_title_user: название листа, с которого забирать информацию о пользователе
    :param ws_title_product: название листа, с которого забирать информацию о средствах

    :return: объединенный из 2х словарей словарь с параметрами о
    человеке и информацией о средствах

    """

    dict_with_info = _load_info_about_user(
        file_path=file_path,
        ws_title=ws_title_user,
    )

    dict_with_product = _load_info_about_products(
        file_path=file_path,
        ws_title=ws_title_product,
    )

    # Формирование общего словаря
    return {
        "Пользователь": dict_with_info,
        "Средства": dict_with_product["Средства"],
    }


if __name__ == '__main__':
    print(
        main(
            file_path='../00_base/00_Средства.xlsx',
            ws_title_user='Подборки',
            ws_title_product='Средства',
        )
    )
