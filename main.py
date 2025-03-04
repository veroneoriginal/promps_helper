"""В этом модуле запуск логики анализа средств и формирования отчета"""

from control_manager.control_manager import ControlManager
from source.structure_folders.structure_folders import scheme_for_folders_name

control_manager = ControlManager(
    scheme_for_folders=scheme_for_folders_name
)
control_manager.create_collection(
    file_path_tools='00_base/Средства.xlsx',
    file_path_collection='00_base/Подборки.xlsx',
    path_to_output_folder='00_base/00_info_for_post/',
)
