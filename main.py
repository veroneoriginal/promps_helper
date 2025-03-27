"""В этом модуле запуск логики анализа средств и формирования отчета"""

from control_manager.control_manager import ControlManager
# словарь со всеми параметрами для разных категорий продуктов
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

if __name__ == '__main__':
    control_manager = ControlManager(
        param_dif_products_categories=PARAMETERS_DIF_PRODUCT_CATEGORIES,
    )
    control_manager.create_collection(
        file_path_tools='00_base/Средства.xlsx',
        # file_path_tools='00_base/Средства_копия.xlsx',
        file_path_collection='00_base/Подборки.xlsx',
        # file_path_collection='00_base/Подборки для тестов.xlsx',
        path_to_output_folder='00_base/00_info_for_post/',
        checking_unique=True,
    )
