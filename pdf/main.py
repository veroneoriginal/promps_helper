# pylint: disable=E0611: no-name-in-module
import copy
import os

from pdf.creator_logic.creator.document_creator import PDFConverterToImage
from pdf.creator_logic.main import PDFCreator
from pdf.pdf_data_processing.main import PDFDataProcessor
from pdf.textpost_pdf_creator.main import PDFTextPostProcessor
from pdf.utils import _get_pdf_file_paths, copy_image_if_needed


def create_pdf(
        collection_data: dict,
        info_data: dict,
        selection_result: dict,
        path_to_output_folder_pdf_file: str,
        path_to_output_folder_jpg_file: str,
) -> None:
    """
    Готовит PDF и изображения

    :param collection_data: Данные подборки
    :param info_data: данные со всеми средствами, врачами и т.д.
    :param selection_result: Данные с результатом нейронки по подборке
    :param path_to_output_folder_pdf_file: путь к папке для сохранения PDF-файлов
    :param path_to_output_folder_jpg_file: путь к папке для сохранения JPG-файлов
    :return: None
    """

    copy_data_collection = copy.deepcopy(collection_data)

    pdf_data_processor = PDFDataProcessor(
        collection_data=copy_data_collection,
        info_data=info_data,
        selection_result=selection_result,
        path_to_output_folder_pdf_file=path_to_output_folder_pdf_file,
    )
    data_for_pdf = pdf_data_processor.process_data_with_task_code()

    # Генерируем pdf и сохраняем по указанному в данных пути
    pdf_creator = PDFCreator(
        data_for_pdf=data_for_pdf,
    )
    pdf_creator.create_pdf()

    # Получаем пути всех PDF-файлов, размеры для конвертации в изображения и
    # пути для сохранения в JPEG
    pdf_file_paths = _get_pdf_file_paths(
        input_data=data_for_pdf,
        path_to_output_folder_jpg_file=path_to_output_folder_jpg_file,
    )
    # Конвертируем pdf в изображения
    pdf_converter = PDFConverterToImage(
        file_paths=pdf_file_paths,

    )
    pdf_converter.convert_to_image()
    copy_image_if_needed(
        folder_path=path_to_output_folder_jpg_file,
        task=collection_data['Задача']
    )


def create_textpost_pdf(
        path_to_text_post_file: str,
        path_for_save_pdf_file: str,
) -> None:
    """
   :param path_to_text_post_file: путь к файлу с текстовым постом
   :param path_for_save_pdf_file: путь для сохранения pdf-файлов

   :return: None
   """

    pdf_data_processor = PDFTextPostProcessor(
        path_to_text_post_file=path_to_text_post_file,
        path_for_save_pdf_file=path_for_save_pdf_file,
    )
    # создаём PDF из текстового поста
    pdf_data_processor.create_textpost_pdf()
    path_for_save_jpg_file = path_for_save_pdf_file.rsplit('.', 1)[0] + '.jpg'

    # Конвертируем pdf в изображение
    convert_pdf_data = {
        path_for_save_pdf_file: {
            'size': (1024, 1280),
            'jpg_file_name': path_for_save_jpg_file,
        }
    }
    pdf_converter = PDFConverterToImage(
        file_paths=convert_pdf_data,
    )
    pdf_converter.convert_to_image()

    # удаляем pdf
    os.remove(path_for_save_pdf_file)
