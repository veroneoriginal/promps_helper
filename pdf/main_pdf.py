import os
from typing import List
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import (
    TA_LEFT,
    TA_RIGHT,
    TA_CENTER,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Image,
    Flowable,
)
from pdf2image import convert_from_path


class PDFCreator:
    """Класс для создания pdf файлов"""

    def __init__(self):
        self._registration_fonts()
        self.my_style = self._create_style()
        self.width_page = 1024  # Ширина страницы в пикселях
        self.heigth_page = 1280  # Высота страницы в пикселях

    def _registration_fonts(self) -> None:
        """
        Метод для регистрации шрифтов для проекта

        :return: None
        """

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVuSansBold", "DejaVuSans-Bold.ttf"))

    def _create_style(self) -> dict:
        """
        Метод для задания параметров стиля

        :return: словарь со стилями
        """

        return {
            # стиль названия средства
            'title_style': ParagraphStyle(
                'Title',
                fontName="DejaVuSansBold",
                fontSize=25,
                spaceBefore=20,
                spaceAfter=20,
                alignment=TA_CENTER,
                leftIndent=50,
                leading=30,
            ),
            # стиль соотношения мл/руб
            'ratio_align_style': ParagraphStyle(
                'RightAlign',
                fontName="DejaVuSansBold",
                fontSize=18,
                alignment=TA_RIGHT,
            ),
            # стиль плюсы/минусы
            'bold_style': ParagraphStyle(
                'Bold',
                fontName="DejaVuSansBold",
                fontSize=21,
                spaceBefore=10,
                spaceAfter=10,
                alignment=TA_LEFT,
                leftIndent=50,
            ),
            # стиль описания плюсов и минусов
            'normal_style': ParagraphStyle(
                'Normal',
                fontName="DejaVuSans",
                fontSize=16,
                spaceBefore=15,
                spaceAfter=10,
                leftIndent=50,
                leading=20,
            ),
        }

    def _pixels_to_points(
            self,
            pixels: int | float,
    ) -> int | float:
        """
        Метод для конвертирования пикселей в поинты.

        В типографике поинты (pt) используются как единицы измерения.
        В reportlab и PDF стандартный DPI (dots per inch) = 72 dpi.
        В экранах и изображениях стандартный DPI = 96 dpi.
        Поэтому, чтобы перевести из 96 dpi → 72 dpi,
        используется коэффициент 72 / 96 = 0.75.

        :param pixels: значение изображения в пикселях
        :return: значение изображения в поинтах
        """

        return pixels * 72 / 96

    # pylint: disable=W0718 (broad-exception-caught
    def _add_product_image(
            self,
            elements: list,
            img_path: str,
    ) -> None:
        """
        Метод для добавления изображения продукта/средства с правильным масштабированием.

        :param elements: список, в который добавляются элементы для отрисовки в PDF.
        :param img_path: путь к изображению, которое нужно вставить
        :return: None - (изменяет переданный список elements, добавляя в него изображение).
        """
        try:
            img = Image(img_path,
                        width=self._pixels_to_points(pixels=self.width_page),
                        height=self._pixels_to_points(pixels=self.heigth_page),
                        kind='proportional')
            elements.append(Spacer(1, -80))
            elements.append(img)
        except Exception as exc:
            print(f"Ошибка загрузки изображения {img_path}: {exc}")

    def _add_product_info(
            self,
            elements: list,
            product: dict,
    ) -> None:
        """
        Добавляет текстовую информацию о продукте на страницу.

        :param elements: список, в который добавляются элементы для отрисовки в PDF.
        :param product: словарь, из которого берется информация по конкретному продукту.

        :return: None (изменяет переданный список elements,
        добавляя в него информацию по продукту).
        """

        elements.append(Spacer(1, 15))
        elements.append(Paragraph(product.get("Название", ""),
                                  self.my_style['title_style']))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"{product.get('Соотношение', '')}",
                                  self.my_style['ratio_align_style']))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<b>Плюсы:</b>", self.my_style['bold_style']))
        elements.append(Paragraph(product.get("Плюсы", ""), self.my_style['normal_style']))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<b>Минусы:</b>", self.my_style['bold_style']))
        elements.append(Paragraph(product.get("Минусы", ""), self.my_style['normal_style']))

    def _add_base_doc_template(
            self,
            output_file: str,
    ) -> BaseDocTemplate:
        """
        Метод для создания базового шаблона PDF-документа.

        :param output_file: путь, куда будет сохранен PDF-файл.

        :return: объект BaseDocTemplate, представляющий структуру документа
        """

        return BaseDocTemplate(
            output_file,
            pagesize=(
                self._pixels_to_points(self.width_page),
                self._pixels_to_points(self.heigth_page),
            ),
        )

    def _add_frame_for_elements(
            self,
            doc: BaseDocTemplate,
    ) -> Frame:
        """
        Этот метод создает и возвращает объект Frame, который определяет область
        на странице, в которой будут размещаться элементы (flowables) внутри BaseDocTemplate.

        Фрейм (`Frame`) занимает всю доступную область документа,
        используя его отступы, ширину и высоту.
        В нем будут размещаться текстовые блоки, изображения и другие элементы PDF.

        :param doc: объект BaseDocTemplate, который содержит параметры страницы.

        :return: объект Frame, определяющий область для размещения элементов.
        """
        return Frame(
            doc.leftMargin,  # Отступ слева
            doc.bottomMargin,  # Отступ снизу
            doc.width,  # Ширина фрейма (равна ширине страницы)
            doc.height,  # Высота фрейма (равна высоте страницы)
            id='normal',  # Идентификатор фрейма
        )

    def _choosing_brand_line(
            self,
            product: dict,
    ) -> str:
        """
        Метод для выбора бренд‑линии

        :param product: словарь с информацией о продукте
        :return: строка с путем до выбранной брендированной линии
        """

        if product.get('Лучшее средство'):
            return "00_base/imagine_border/border_green.jpg"

        return "00_base/imagine_border/border_fiolet.jpg"

    def _on_page_end_wrapper(
            self,
            product: dict,
    ) -> callable:
        """
        Метод — обертка (wrapper) для _draw_brand_line(),
        которая позволяет передавать product в обработчик события onPageEnd.

        ReportLab ожидает, что onPageEnd принимает только (canvas, doc),
        но метод draw_brand_line требует дополнительного параметра product.
        Эта обертка решает проблему, создавая функцию wrapped,
        которая передает product внутрь draw_brand_line.

        :param product: словарь с информацией о продукте.
        :return: вложенная функция wrapped, которая будет вызвана в onPageEnd.
        """

        def wrapped(canvas, doc):
            self._draw_brand_line(canvas, doc, product)

        return wrapped

    # pylint: disable=W0613 unused-argument
    def _draw_brand_line(self,
                         canvas: 'Canvas',
                         doc: BaseDocTemplate,
                         product: dict,
                         ):
        """
        Функция для отрисовки бренд-линии

        :param canvas: объект ReportLab canvas
        :param product: словарь с информацией о продукте
        :param doc: объект документа ReportLab
        :return: объект брендированной линии на листе
        """

        return canvas.drawImage(
            self._choosing_brand_line(product=product),
            0,  # x (левый край)
            0,  # y (нижний край)
            width=self._pixels_to_points(pixels=80),  # фиксированная ширина линии
            height=self._pixels_to_points(pixels=self.heigth_page),  # фиксированная высота линии
            # параметр управляет сохранением пропорции изображения при его масштабировании.
            preserveAspectRatio=False,
            anchor='sw',  # Привязка к нижнему левому углу
        )

    def _painting_brand_line(
            self,
            frame: Frame,
            product: dict,
    ) -> PageTemplate:
        """
        Метод для отрисовки бренд - линии, внутри которого
        создается PageTemplate с использованием onPageEnd.

        onPageEnd - специальный обработчик событий в ReportLab,
        который вызывается в конце каждой страницы PDF.
        Он позволяет выполнить кастомные действия перед тем,
        как страница будет зафиксирована в PDF.

        :param frame: объект Frame, определяющий область для размещения элементов.
        :param product: словарь с информацией о продукте
        :return: шаблон страницы, который будет использоваться в PDF
        """

        return PageTemplate(
            id='normal',
            frames=[frame],
            onPageEnd=self._on_page_end_wrapper(product=product),
        )

    def _create_flowables(
            self,
            product: dict,
    ) -> List[Flowable]:

        """
        Метод для создания flowables - это список элементов
        (изображений, текста, отступов), которые добавляются в PDF

        :param product: словарь с информацией о продукте
        :return: список flowables (изображений, текста и других элементов)
        """

        flowables = []
        self._add_product_image(flowables, product.get("Ссылка на изображение в базе", ""))
        self._add_product_info(flowables, product)

        return flowables

    def _convert_pdf_to_jpg(
            self,
            output_folder_jpg: str,
            output_file: str,
    ) -> None:
        """
        Конвертирует PDF в JPG.

        :param output_folder_jpg: папка, в которую сохранять JPG.
        :param output_file: путь к PDF-файлу, который нужно конвертировать.
        :return: None
        """

        os.makedirs(output_folder_jpg, exist_ok=True)

        # Конвертация PDF в изображения
        images = convert_from_path(output_file)
        safe_filename = os.path.basename(output_file).replace(".pdf", "")

        for _, img in enumerate(images):
            jpg_filename = os.path.join(
                output_folder_jpg,
                f"{safe_filename}.jpg",
            )
            # Сохраняем как JPG
            img.save(jpg_filename, "JPEG")


    def create_pdf_for_telegram(
            self,
            list_with_info: list,
            output_folder_pdf: str,
            output_folder_jpg: str,
    ) -> None:
        """
        Создает PDF-файлы с наложенной бренд‑линей поверх основного контента.

        :param list_with_info: список словарей с информацией о продуктах.
        :param output_folder_pdf: папка для сохранения PDF.
        :param output_folder_jpg: папка для сохранения JPG.

        :return: None
        """

        os.makedirs(output_folder_pdf, exist_ok=True)

        for product in list_with_info:
            product_name = product.get("Название")
            safe_filename = product_name.replace(" ", "_").replace("/", "_") + ".pdf"
            output_file = os.path.join(output_folder_pdf, safe_filename)

            # Метод для создания BaseDocTemplate
            doc = self._add_base_doc_template(output_file=output_file)

            # Создаем фрейм для основных элементов (flowables)
            frame = self._add_frame_for_elements(doc=doc)

            # Функция для отрисовки бренд - линии
            template = self._painting_brand_line(
                frame=frame,
                product=product,
            )

            # добавление страницы в документ
            doc.addPageTemplates([template])

            # наполняем список нужными элементами
            flowables = self._create_flowables(product=product)

            # собираем документ
            doc.build(flowables)

            # конвертируем pdf в jpg
            self._convert_pdf_to_jpg(
                output_folder_jpg=output_folder_jpg,
                output_file=output_file,
            )
