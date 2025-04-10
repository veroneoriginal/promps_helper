"""В этом модуле запуск пересоздания PDF и текстовых постов"""

from control_manager.main import ControlManager

if __name__ == '__main__':
    control_manager = ControlManager()
    control_manager.recreate_pdf_and_posts(
        file_path_tools='00_base/Средства_АКТУАЛЬНАЯ.xlsx',
        file_path_collection='00_base/Подборки_мои.xlsx',
        path_to_output_folder='00_base/00_info_for_post/',
    )
