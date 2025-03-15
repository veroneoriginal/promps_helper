"""В этом модуле запуск логики анализа средств и формирования отчета"""

from control_manager.control_manager import ControlManager
# словарь с данными для формирования путей для сохраненяи данных
from source.structure_folders import scheme_for_folders_name
# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

if __name__ == '__main__':
    control_manager = ControlManager(
        scheme_for_folders=scheme_for_folders_name,
        param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES
    )
    control_manager.create_collection(
        file_path_tools='00_base/Средства.xlsx',
        file_path_collection='00_base/Подборки.xlsx',
        path_to_output_folder='00_base/00_info_for_post/',
    )
