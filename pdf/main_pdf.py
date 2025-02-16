import os
from pathlib import Path
from typing import (
    Tuple,
    List,
)

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import (
    TA_LEFT,
    TA_RIGHT,
    TA_CENTER,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Image,
)
from pdf2image import convert_from_path


class PDFCreator:
    """Класс для создания pdf файлов"""

    def __init__(self):
        self._registration_fonts()
        self.my_style = self._create_style()
        self.sizes = None  # Ширина и высота страницы в пикселях
        self.flowables = []

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
            img_path: str,
    ) -> None:
        """
        Метод для добавления изображения продукта/средства с правильным масштабированием.

        :param img_path: путь к изображению, которое нужно вставить
        :return: None - (изменяет переданный список self.flowables, добавляя в него изображение).
        """
        try:
            img = Image(img_path,
                        width=self._pixels_to_points(pixels=self.sizes[0]),
                        height=self._pixels_to_points(pixels=self.sizes[1]),
                        kind='proportional')
            self.flowables.append(Spacer(1, -80))
            self.flowables.append(img)
        except Exception as exc:
            print(f"Ошибка загрузки изображения {img_path}: {exc}")

    def _add_product_info(
            self,
            product: dict,
    ) -> None:
        """
        Добавляет текстовую информацию о продукте на страницу.

        :param product: словарь, из которого берется информация по конкретному продукту.

        :return: None (изменяет переданный список self.flowables,
        добавляя в него информацию по продукту).
        """

        self.flowables.append(Spacer(1, 15))
        self.flowables.append(Paragraph(product.get("Название", ""),
                                        self.my_style['title_style']))

        self.flowables.append(Spacer(1, 10))
        self.flowables.append(Paragraph(f"{product.get('Соотношение', '')}",
                                        self.my_style['ratio_align_style']))

        self.flowables.append(Spacer(1, 10))
        self.flowables.append(Paragraph("<b>Плюсы:</b>", self.my_style['bold_style']))
        self.flowables.append(Paragraph(product.get("Плюсы", ""), self.my_style['normal_style']))

        self.flowables.append(Spacer(1, 10))
        self.flowables.append(Paragraph("<b>Минусы:</b>", self.my_style['bold_style']))
        self.flowables.append(Paragraph(product.get("Минусы", ""), self.my_style['normal_style']))

    def _add_base_doc_template(
            self,
            output_file,
    ) -> BaseDocTemplate:
        """
        Метод для создания базового шаблона PDF-документа.

        :param output_file: путь, куда будет сохранен PDF-файл.
        :return: объект BaseDocTemplate, представляющий структуру документа.
        """

        return BaseDocTemplate(
            filename=output_file,
            pagesize=(
                self._pixels_to_points(self.sizes[0]),
                self._pixels_to_points(self.sizes[1]),
            ),
        )

    def _create_frame_for_elements(
            self,
            x1_y1: Tuple[float, float],
            width_height: Tuple[float, float],
            frame_id: str = 'body_frame',
    ) -> Frame:
        """
        Этот метод создает и возвращает объект Frame, который определяет область
        на странице, в которой будут размещаться элементы (flowables)
        внутри BaseDocTemplate.

        x1 и y1 - координаты нижнего левого угла фрейма
        width и height - ширина и высота фрейма

        :param x1_y1: кортеж с координатами нижнего угла для фрейма
        :param width_height: кортеж с шириной и высотой фрейма
        :param frame_id: идентификатор (имя) фрейма

        :return: объект Frame, определяющий область для размещения элементов.
        """

        return Frame(
            x1=x1_y1[0],
            y1=x1_y1[1],
            width=width_height[0],
            height=width_height[1],
            id=frame_id,
            # showBoundary=True,
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
            return "00_base/course/imagine_border/border_green.jpg"
        return "00_base/course/imagine_border/border_fiolet.jpg"

    def _on_page_end_brand_line_wrapper(
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
        С помощью замыкания мы решаем проблему передачи дополнительного
        аргумента.

        :param product: словарь с информацией о продукте.
        :return: вложенная функция wrapped, которая будет вызвана в onPageEnd.
        """

        def wrapped(canvas, doc):
            self._draw_brand_line(canvas, doc, product)

        return wrapped

    # pylint: disable=W0613 unused-argument
    def _draw_brand_line(
            self,
            canvas: Canvas,
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
            image=self._choosing_brand_line(product=product),
            x=0,  # x (левый край)
            y=0,  # y (нижний край)
            width=self._pixels_to_points(pixels=80),  # фиксированная ширина линии
            height=self._pixels_to_points(pixels=self.sizes[1]),  # фиксированная высота линии
        )

    def _create_page_template(
            self,
            frames: List[Frame],
            on_page_end: callable,
            tempalate_id: str = 'base_page',
    ) -> PageTemplate:
        """
        Метод для создания шаблона страницы.
        onPageEnd - специальный обработчик событий в ReportLab,
        который вызывается в конце каждой страницы PDF.
        Он позволяет выполнить кастомные действия перед тем,
        как страница будет зафиксирована в PDF.
        Создается PageTemplate с использованием onPageEnd.

        :param frames: список объектов Frame, определяющих области для размещения элементов.
        :param tempalate_id: идентификатор (имя) шаблона страницы
        :param on_page_end: функция, которая будет вызвана в конце перед финальным
        созданием страницы
        :return: шаблон страницы, который будет использоваться в PDF
        """

        return PageTemplate(
            id=tempalate_id,
            frames=frames,
            onPageEnd=on_page_end,
        )

    def _fill_flowables_six_products(
            self,
            product: dict,
    ) -> None:
        """
        Метод для создания flowables - это список элементов
        (изображений, текста, отступов), которые добавляются в PDF

        :param product: словарь с информацией о продукте
        :return: обновляет список flowables (изображений, текста и других элементов)
        """
        self._add_product_image(product.get("Ссылка на изображение в базе", ""))
        self._add_product_info(product)

    def _convert_pdf_to_jpg(
            self,
            output_folder_jpg: Path,
            output_file: Path,
    ) -> None:
        """
        Конвертирует PDF в JPG.

        :param output_folder_jpg: папка, в которую сохранять JPG.
        :param output_file: путь к PDF-файлу, который нужно конвертировать.
        :return: None
        """

        os.makedirs(output_folder_jpg, exist_ok=True)

        # Конвертация PDF в изображения
        images = convert_from_path(
            pdf_path=output_file,
            size=self.sizes
        )
        safe_filename = os.path.basename(output_file).replace(".pdf", "")

        for _, img in enumerate(images):
            jpg_filename = os.path.join(
                output_folder_jpg,
                f"{safe_filename}.jpg",
            )
            # Сохраняем как JPG
            img.save(jpg_filename, "JPEG")

    def _format_product_filename(
            self,
            product: dict,
            output_folder_pdf: Path,
    ) -> Path:
        """
        Метод для форматирования имя файла продукта

        :param output_folder_pdf: путь (Path) к папке для сохранения PDF.
        :param product: словарь со средством и его параметрами

        :return: полный путь к файлу PDF
        """
        product_name = product.get("Название")
        safe_filename = product_name.replace(" ", "_").replace("/", "_") + ".pdf"

        return output_folder_pdf / safe_filename

    def _create_doctemplate_six_products(
            self,
            output_file: Path,
            product: dict,
    ) -> BaseDocTemplate:

        """
        Создает и настраивает PDF-документ (`BaseDocTemplate`) c одним главным
        фреймом. В обработчик шаблона станицы передаём функцию для отрисовки бренд-линии.

        :param output_file: путь, по которому будет сохранен PDF-файл.
        :param product: словарь с инфо о продукте, который используется для отрисовки бренд-линии.
        :return: готовый шаблон документа для дальнейшего заполнения.
        """

        # Метод для создания BaseDocTemplate
        doc = self._add_base_doc_template(output_file=str(output_file))

        # Создаем фрейм для основных элементов (flowables)
        frame = self._create_frame_for_elements(
            x1_y1=(doc.leftMargin, 0),
            width_height=(doc.width, doc.height + doc.bottomMargin),
            frame_id='body_frame'
        )

        # Создаём шаблон страницы
        # В on_page_end мы передаём функцию отрисовки линии бренда поверх других
        # элементов с помощью канвы, а не flowebles.
        template = self._create_page_template(
            frames=[frame,],
            on_page_end=self._on_page_end_brand_line_wrapper(product=product),
        )

        # добавление шаблона страницы в документ
        doc.addPageTemplates([template])

        return doc

    def _build_document(
            self,
            doc: BaseDocTemplate,
    ) -> None:
        """
        Строит PDF-документ с переданными flowables.

        :param doc: объект BaseDocTemplate (шаблон PDF-документа).

        :return: None
        """
        doc.build(self.flowables)

    def gen_pages_for_six_product(
            self,
            list_with_info: list,
            output_folder_pdf: Path,
            output_folder_jpg: Path,
    ) -> None:
        """
        Создает PDF-файлы с наложенной бренд‑линей поверх основного контента.

        :param list_with_info: список словарей с информацией о продуктах.
        :param output_folder_pdf: путь (Path) к папке для сохранения PDF.
        :param output_folder_jpg: путь (Path) к папке для сохранения JPG.

        :return: None
        """
        output_folder_pdf.mkdir(parents=True, exist_ok=True)
        self.sizes = (1024, 1280)  # Ширина и высота страницы в пикселях

        for product in list_with_info:
            # форматируем имя файла
            output_file = self._format_product_filename(
                product=product,
                output_folder_pdf=output_folder_pdf,
            )

            # наполняем шаблон
            doc = self._create_doctemplate_six_products(
                output_file=output_file,
                product=product,
            )

            # наполняем список нужными элементами
            self._fill_flowables_six_products(product=product)

            # собираем документ
            self._build_document(doc=doc)

            # конвертируем pdf в jpg
            self._convert_pdf_to_jpg(
                output_folder_jpg=output_folder_jpg,
                output_file=output_file,
            )
