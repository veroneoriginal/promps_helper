# pylint: disable=W0212 protected-access
import json

from control_manager.main import ControlManager
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES


def get_data_tools_for_test():
    """
    Записываем в модуль "data_tools_for_test.py"
    словарь из "базы данных" книги "Средства.xlsx"
    """
    control_manager = ControlManager(
        param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
    )

    # Забираю все данные из таблицы "Средства", "Тип", "Запрос" и т.д.
    data_tools = control_manager._take_data_from_table_tool(
        file_path_tools_table='00_base/Средства_АКТУАЛЬНАЯ.xlsx',
    )

    with open("dev_helpers/data.json", "w", encoding="utf-8") as file:
        json.dump(data_tools, file, indent=4, ensure_ascii=False)
