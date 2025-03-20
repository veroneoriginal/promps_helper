from pathlib import Path


def _get_pdf_file_paths(
        input_data: list,
        path_to_output_folder_jpg_file: str,
) -> dict:
    """
    Возвращает словарь вида:
    {путь к PDF-файлу: {size:  размеры документа, jpg_file_name: путь для сохранения jpg})
    :param input_data: список с словарями данных по каждому средству
    :param path_to_output_folder_jpg_file: путь к папке для сохранения JPG-файлов

    :return: словарь с путями и размерами
    """
    output_data = {}
    output_folder = Path(path_to_output_folder_jpg_file)

    for product in input_data:
        pdf_file_path = Path(product.get('Путь для сохранения pdf-файла'))
        size = product.get('Размеры документа')

        # Меняем расширение .pdf → .jpg
        jpg_file_name = pdf_file_path.with_suffix(".jpg").name

        output_data[pdf_file_path] = {
            "size": size,
            "jpg_file_name": output_folder / jpg_file_name,
        }

    return output_data
