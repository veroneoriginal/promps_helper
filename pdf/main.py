# pylint: disable=E0611: no-name-in-module
from pdf.creator_logic.creator.document_creator import PDFConverterToImage
from pdf.creator_logic.main import PDFCreator
from pdf.pdf_data_processing.main import PDFDataProcessor
from pdf.utils import _get_pdf_file_paths


def create_pdf(
        collection_data: dict,
        info_data: dict,
        selection_result: dict,
        path_to_output_folder_pdf_file: str,
        path_to_output_folder_jpg_file: str,
) -> None:
    """
    Готовит PDF и изображения

    :param collection_data: данные подборки
    :param info_data: данные с всеми средствами, врачами и т.д.
    :param selection_result: данные с результатом нейронки по подборке
    :param path_to_output_folder_pdf_file: путь к папке для сохранения PDF-файлов
    :param path_to_output_folder_jpg_file: путь к папке для сохранения JPG-файлов
    :return: None
    """

    pdf_data_processor = PDFDataProcessor(
        collection_data=collection_data,
        info_data=info_data,
        selection_result=selection_result,
        path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
    )
    collection_data = pdf_data_processor.process_data_with_task_code()

    # Генерируем pdf и сохраняем по указанному в данных пути
    pdf_creator = PDFCreator(
        collection_data=collection_data,
    )
    pdf_creator.create_pdf()

    # Получаем пути всех PDF-файлов, размеры для конвертации в изображения и
    # пути для сохранения в JPEG
    pdf_file_paths = _get_pdf_file_paths(
        input_data=collection_data['Данные'],
        path_to_output_folder_jpg_file=path_to_output_folder_jpg_file,
    )
    # Конвертируем pdf в изображения
    pdf_converter = PDFConverterToImage(
        file_paths=pdf_file_paths,

    )
    pdf_converter.convert_to_image()
