from pathlib import Path

from pdf.creator_logic.creator.document_creator import (
    PDFBaseDocTemplateWithBrandLine,
    PDFPageTemplateandFrameBuilder,
)
from pdf.textpost_pdf_creator.utils import create_emodji_flowables


class PDFTextPostProcessor:
    """
    Класс для создания PDF из текстовых постов
    """

    def __init__(
            self,
            path_to_text_post_file: str,
            path_for_save_pdf_file: str,

    ) -> None:
        """
        :param path_to_text_post_file: путь к файлу с текстовым постом
        :param path_for_save_pdf_file: путь для сохранения pdf-файлов

        :return: None
        """

        self.path_to_text_post_file = path_to_text_post_file
        self.path_for_save_pdf_file = path_for_save_pdf_file

    def read_text_post(self, file_path) -> str:
        """
        Читает текстовый пост из .md файла
        :return: строка с текстом поста
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def create_textpost_pdf(self):
        """
        Создаёт из текстового поста PDF-документ

        """
        text = self.read_text_post(file_path=self.path_to_text_post_file)
        doc = PDFBaseDocTemplateWithBrandLine(
            filename=self.path_for_save_pdf_file,
            path_to_brandline_file=Path("00_base/source/imagine_border/border_green.jpg"),
            doc_width_height=(1024, 1280),
            brand_line_width_height=(85, 1280),
            brand_line_coords=[(0, 0), ],
        )
        page_frames = {
            'template_1':
                (
                    # Номер, Координаты левого нижнего угла, ширина и высота фрейма
                    (0, (110, 0), (850, 1250)),
                ),
        }
        # Создаём шаблоны страниц с фреймами
        page_templates_builder = PDFPageTemplateandFrameBuilder()
        templates = page_templates_builder.create_doc_templates(
            templates_data=page_frames
        )
        doc.addPageTemplates(templates)

        story = create_emodji_flowables(text)
        doc.build(story)
