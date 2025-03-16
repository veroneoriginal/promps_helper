from pdf.creator_logic.creator.document_creator import (
    PDFBaseDocTemplateWithBrandLine,
    PDFFlowablesCreator,
    PDFPageTemplateandFrameBuilder,
)


class PDFCreator:
    """
    Создаёт PDF-документ и изображения из них
    """

    def __init__(self, collection_data: dict):
        """
        :param collection_data: Словарь с данными по всей подборке
        """
        self.collection_data = collection_data

    def create_pdf(self):
        """
        Создаёт PDF-документ из входящих данных
        """

        for data in self.collection_data['Данные']:
            # Создаём документ
            doc = PDFBaseDocTemplateWithBrandLine(
                filename=str(data['Путь для сохранения pdf-файла']),
                path_to_brandline_file=data['Путь к изображению бренд-линии'],
                doc_width_height=(
                    data['Размеры документа'][0],
                    data['Размеры документа'][1]
                ),
                brand_line_width_height=(
                    data['Размеры бренд-линии'][0],
                    data['Размеры бренд-линии'][1]
                )
            )

            # Создаём flowables-элементы документа
            pdf_flowables_creator = PDFFlowablesCreator(data=data)
            flowables = pdf_flowables_creator.create_flowables()

            # Создаём шаблоны страниц с фреймами
            page_templates_builder = PDFPageTemplateandFrameBuilder()
            templates = page_templates_builder.create_doc_templates(
                templates_data=data['Шаблоны страниц с фреймами']
            )

            # добавление шаблона страницы в документ
            doc.addPageTemplates(templates)

            # рендер PDF-документа
            doc.build(flowables)
