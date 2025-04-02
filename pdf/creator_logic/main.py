from pdf.creator_logic.creator.document_creator import (
    PDFFlowablesCreator,
    PDFPageTemplateandFrameBuilder,
    TEMPLATE_CLASS,
)


class PDFCreator:
    """
    Создаёт PDF-документ и изображения из них
    """

    def __init__(self, data_for_pdf: list):
        """
        :param data_for_pdf: список с данными для генерации PDF
        """
        self.data_for_pdf = data_for_pdf

    def create_pdf(self):
        """
        Создаёт PDF-документ из входящих данных
        """

        for data in self.data_for_pdf:
            template_class = TEMPLATE_CLASS[data['Класс шаблона']]

            # Создаём документ
            doc = template_class(
                filename=str(data['Путь для сохранения pdf-файла']),
                path_to_brandline_file=data['Путь к изображению бренд-линии'],
                doc_width_height=(
                    data['Размеры документа'][0],
                    data['Размеры документа'][1]
                ),
                brand_line_width_height=(
                    data['Размеры бренд-линии'][0],
                    data['Размеры бренд-линии'][1]
                ),
                brand_line_coords=data['Координаты вставки бренд-линии']
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
