"""В этом модуле запуск логики анализа средств и формирования отчета"""

from control_manager.main import ControlManager

if __name__ == '__main__':
    control_manager = ControlManager()
    control_manager.create_collection(
        file_path_tools='00_base/Средства_АКТУАЛЬНАЯ.xlsx',
        file_path_collection='00_base/Подборки_мои.xlsx',
        path_to_output_folder='00_base/00_info_for_post/',
    )
