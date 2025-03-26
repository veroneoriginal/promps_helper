from dev_helpers.get_data_tools import get_data_tools_for_test

if __name__ == "__main__":
    """
    При запуске модуля:
    1) в файл "dev_helpers/data.json" записывается весь словарь со всеми данными из 
    книги '00_base/Средства.xlsx'
    2) из модуля "dev_helpers/data_tools_for_test" можно забирать в тесты ALL_DATA_TOOLS_FOR_TEST
    НЕ ЗАБУДЬ сначала спарсить средства, чтобы были изображения
    """
    get_data_tools_for_test()
