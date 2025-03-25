from datetime import datetime
from pathlib import Path

from source.structure_folders import SCHEME_FOR_FOLDERS_NAME


class DirsConstructor:
    """
    Создаёт необходимые папки для сохранения информации подборки.
    """

    def __init__(
            self,
            base_output_folder_path: str,
            data_collection: dict,
            scheme_for_folders_name: dict = None,
    ):
        """
        :param base_output_folder_path: путь к базовой папке,
        например '00_base/00_info_for_post/'
        :param data_collection: данные с подборкой,
        :param scheme_for_folders_name: схема для создания папок и путей,

        """
        self.base_output_folder_path = base_output_folder_path
        self.scheme_for_folders_name = scheme_for_folders_name or SCHEME_FOR_FOLDERS_NAME
        self.data_collection = data_collection
        # формируемый словарь с путями
        self.paths_to_folders = {}

    def get_output_folders(self) -> dict:
        """
        Метод для создания папки для сохранения файлов.

        :return: dict с путями
        """

        # Определяем базовую папку
        base_output_folder = self._create_timestamped_folder(
            path_to_output_folder=self.base_output_folder_path
        )

        # Получаем список существующих папок в базовой директории
        existing_folders = self._get_existing_folders(
            base_output_folder=base_output_folder,
        )

        # Определяем новый номер папки
        new_folder_number = self._get_new_folder_number(
            existing_folders=existing_folders,
        )

        # Формируем имя новой папки - номер и с чем подборка
        category_folder = self._create_category_folder(
            base_output_folder=base_output_folder,
            new_folder_number=new_folder_number,
            category=self.data_collection['Категория'],
        )

        # Наполняем self.paths_to_folders путями до каждой конкретной папки
        self._get_folder_paths(category_folder=category_folder)

        # Создаем папки для соц.сетей и их внутренние папки с категориями
        self._create_subfolders()

        # Добавляем общий путь к подборке
        self.paths_to_folders['folder_path'] = str(category_folder)

        return self.paths_to_folders

    def _create_timestamped_folder(
            self,
            path_to_output_folder: str,
    ) -> Path:
        """
        Метод для определения базовой папки с текущей датой для сохранения файлов

        :param path_to_output_folder: путь до основной папки, в которую идет сохранение.
        :return: объект Path с путем к базовой папке
        """

        # Получаем текущую дату в формате ДД_ММ_ГГ
        timestamp = datetime.now().strftime("%d_%m_%y")

        # Определяем базовую папку
        base_output_folder = Path(path_to_output_folder) / timestamp
        base_output_folder.mkdir(parents=True, exist_ok=True)

        return base_output_folder

    def _get_existing_folders(
            self,
            base_output_folder: Path,
    ) -> list:
        """
        Метод получает список существующих папок в указанной директории с текущей датой.

        :param base_output_folder: Путь к базовой директории с текущей датой
        :return: список объектов Path, представляющих папки
        """
        existing_folders = []
        for folder in base_output_folder.iterdir():
            if folder.is_dir():
                existing_folders.append(folder)

        return existing_folders

    def _get_new_folder_number(
            self,
            existing_folders: list,
    ) -> int:
        """
        Определяет новый номер для папки на основе существующих папок.

        :param existing_folders: Список объектов Path, представляющих папки
        :return: Новый номер папки
        """

        # если список пустой
        if not existing_folders:
            return 1

        last_number = 0

        for folder in existing_folders:
            name_parts = folder.name.split('_')
            if name_parts[0].isdigit():
                number = int(name_parts[0])
                last_number = max(last_number, number)

        return last_number + 1

    def _create_category_folder(
            self,
            base_output_folder: Path,
            new_folder_number: int,
            category: str,
    ) -> Path:
        """
        Создаёт папку категории с именем, состоящим из номера и названия категории,
        например, 1_Шампуни

        :param base_output_folder: Базовая выходная папка, где будет создана новая папка
        :param new_folder_number: Номер новой папки
        :param category: Название категории
        :return: Путь к созданной папке категории
        """
        category_folder_name = f"{new_folder_number}_{category}"
        category_folder = base_output_folder / category_folder_name
        category_folder.mkdir(exist_ok=True)
        return category_folder

    def _get_folder_paths(
            self,
            category_folder: Path,
    ) -> None:
        """
        Создает словарь путей ко всем созданным папкам соцсетей и их подпапкам.

        :param category_folder: Путь к папке подборки
        :return: None (изменяет self.paths_to_folders)
        """

        for service, folders in self.scheme_for_folders_name.items():
            service_path = category_folder / service

            # Если список подпапок пустой или отсутствует, добавляем только базовый путь сервиса
            if not folders or not isinstance(folders, list):
                self.paths_to_folders[service] = str(service_path)

            for folder in folders:
                key = f"{service}_{folder}"
                # Получаем полный путь и преобразуем в строку
                full_path = str(service_path / folder)
                # записываем в словарь
                self.paths_to_folders[key] = full_path

    def _create_subfolders(self) -> None:
        """
        Проходим по словарю self.paths_to_folders и создаем папки.

        :return: None
        """

        for folder_path in self.paths_to_folders.values():
            # Преобразуем путь в объект Path
            path = Path(folder_path)

            # Создаём папку (parents=True — создаёт все родительские папки,
            # exist_ok=True — не выдаёт ошибку, если папка уже есть)
            path.mkdir(parents=True, exist_ok=True)
