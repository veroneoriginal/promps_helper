from pathlib import Path
from typing import Tuple

from pdf2image import convert_from_path
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Image,
    Spacer,
    Paragraph,
    Frame,
    PageTemplate,
    Flowable,
)

from pdf.creator_logic.creator.fonts_and_styles import BASE_PDF_STYLE


def _pixels_to_points(
        pixels: int | float,
) -> int | float:
    """
    Конвертирование пикселей в поинты.

    В типографике поинты (pt) используются как единицы измерения.
    В reportlab и PDF стандартный DPI (dots per inch) = 72 dpi.
    В экранах и изображениях стандартный DPI = 96 dpi.
    Поэтому, чтобы перевести из 96 dpi → 72 dpi,
    используется коэффициент 72 / 96 = 0.75.

    :param pixels: значение изображения в пикселях
    :return: значение изображения в поинтах
    """

    return pixels * 72 / 96


class PDFPageTemplateandFrameBuilder:
    """
    Создаёт фреймы и шаблоны страниц для PDF-документа
    """

    def _create_frame(
            self,
            x1_y1: Tuple[float, float],
            width_height: Tuple[float, float],
            frame_id: str,
    ) -> Frame:
        """
        Создает и добавляет в список объект Frame, который определяет область
        на странице, в которой будут размещаться элементы (flowables)
        внутри BaseDocTemplate.

        x1 и y1 - координаты нижнего левого угла фрейма
        width и height - ширина и высота фрейма

        :param x1_y1: кортеж с координатами нижнего угла для фрейма
        :param width_height: кортеж с шириной и высотой фрейма
        :param frame_id: идентификатор (имя) фрейма

        :return: None
        """

        return Frame(
            x1=x1_y1[0],
            y1=x1_y1[1],
            width=width_height[0],
            height=width_height[1],
            id=frame_id,
            # showBoundary=True,
        )

    def _create_frames(
            self,
            frames_data: tuple,
    ) -> list[Frame]:
        """
        Создаёт фреймы для шаблона страниц
        :param frames_data: кортеж с скортежами фреймов с данными
        :return: список фреймов
        """
        frames = []
        for frame in frames_data:
            frames.append(
                self._create_frame(
                    frame_id=str(frame[0]),
                    x1_y1=frame[1],
                    width_height=frame[2],
                )
            )
        return frames

    def _create_page_template(
            self,
            frames: list[Frame],
            template_id: str,
    ) -> PageTemplate:
        """
        Создание шаблона страницы.

        :param frames: список объектов Frame, определяющих области для размещения элементов.
        :param template_id: идентификатор (имя) шаблона страницы
        :return: шаблон страницы, который будет использоваться в PDF
        """

        return PageTemplate(
            id=template_id,
            frames=frames,
        )

    def create_doc_templates(
            self,
            templates_data: dict
    ) -> list[PageTemplate]:
        """
        Создаёт шаблоны страниц с фреймами
        :param templates_data: словарь с данными по шаблонам страниц и фреймам
        :return: список готовых шаблонов страниц
        """
        templates = []
        for template_id, frames_data in templates_data.items():
            frames = self._create_frames(frames_data=frames_data)
            template = self._create_page_template(
                frames=frames,
                template_id=template_id
            )
            templates.append(template)

        return templates


class PDFFlowablesCreator:
    """
    Создание flowables-элементы для PDF-документа: абзацы, картинки и т.д.
    """

    def __init__(
            self,
            data,

    ):
        self.data = data
        self.flowables = []

    def create_flowables(self) -> list[Flowable]:
        """
        Cоздаёт flowables-элементы для PDF-документа: абзацы, картинки и т.д.
        :return: список flowables-элементов
        """
        flowables_structure = self.data['Элементы и стили']
        for flowable_number in list(flowables_structure.keys()):
            flowable_object = flowables_structure[flowable_number]
            match flowable_object['Объект']:
                case 'Image':
                    self._create_image(
                        img_path=self.data[flowable_object['Ключ в подборке']],
                        width=flowable_object['width'],
                        height=flowable_object['height'],
                    )
                case 'Paragraph':
                    text = (
                            flowable_object.get('Текст', None)
                            or self.data[flowable_object['Ключ в подборке']]
                    )
                    self._create_paragraph(
                        text=text,
                        style=self._get_style(flowable_object['Стиль']),
                    )
                case 'Spacer':
                    self._create_spacer(
                        width=flowable_object['width'],
                        height=flowable_object['height'],
                    )
        return self.flowables

    def _create_paragraph(
            self,
            text: str,
            style: ParagraphStyle,

    ) -> None:
        """
        Создаёт параграф с текстом и добавляет в общий список
        :param text: текст
        :param style: стиль
        :return: None
        """
        paragraph = Paragraph(
            text=text,
            style=style,
        )
        self.flowables.append(paragraph)

    def _get_style(self, style_name):
        """
        Возвращает объект стиля по имени
        """
        return BASE_PDF_STYLE[style_name]

    def _create_image(
            self,
            img_path: Path,
            width: int,
            height: int
    ) -> None:
        """
        Создаёт изображение и добавляет в общий список
        :param img_path: путь к изображению
        :param width: ширина изображения
        :param height: высота изображения
        :return: None
        """
        img = Image(img_path,
                    width=_pixels_to_points(pixels=width),
                    height=_pixels_to_points(pixels=height),
                    kind='proportional')
        self.flowables.append(img)

    def _create_spacer(
            self,
            width: int,
            height: int
    ) -> None:
        """
        Создаёт spacer и добавляет в общий список
        :param width: ширина spacer
        :param height: высота spacer
        :return: None
        """
        spacer = Spacer(width, height)
        self.flowables.append(spacer)


class PDFConverterToImage:
    """
    Конвертация PDF-документа в изображение
    """

    def __init__(self, file_paths: dict):
        """
        :param file_paths: словарь с путями файлов для конвертации и размерами
        """
        self.file_paths = file_paths

    def convert_to_image(self) -> None:
        """
        Конвертирует PDF в JPG.

        :return: None
        """
        for pdf_file_path, settings in self.file_paths.items():
            pdf_file_path = Path(pdf_file_path)
            jpg_base_name = Path(settings['jpg_file_name'])

            # Конвертация всех страниц PDF-документа в изображения
            images = convert_from_path(
                pdf_path=pdf_file_path,
                size=settings['size']
            )

            # Если в PDF несколько страниц, добавляем индекс к имени файла
            for i, img in enumerate(images, start=1):
                jpg_file = jpg_base_name.with_stem(
                    f"{jpg_base_name.stem}_page_{i}"
                )  # Добавляем `_page_X`
                # Сохраняем изображение
                img.save(jpg_file, "JPEG")


class PDFBaseDocTemplateWithBrandLine(BaseDocTemplate):
    """
    Создаёт шаблон документа с переопределением
    метода afterPage для нанесения бренд линии
    на каждую страницу документа
    """

    def __init__(
            self,
            filename: str,
            doc_width_height: tuple,
            brand_line_width_height: tuple,
            path_to_brandline_file: Path,
            **kwargs
    ):
        """
        :param filename: имя PDF-документа
        :param doc_width_height: ширина и высота документа
        :param brand_line_width_height:  ширина и высота бренд-линии
        :param path_to_brandline_file: путь к файлу с бренд-линией
        """
        self.doc_width_height = doc_width_height
        self.brand_line_width_height = brand_line_width_height
        self.path_to_brandline_file = path_to_brandline_file

        super().__init__(
            filename=filename,
            pagesize=(
                _pixels_to_points(self.doc_width_height[0]),
                _pixels_to_points(self.doc_width_height[1]),
            ),
            **kwargs
        )

    # pylint: disable=W0613: unused-argument
    def _add_brandline(
            self,
            canvas: Canvas,
            doc: BaseDocTemplate,
    ):
        """
        Рисует бренд-линию на канве
        """
        canvas.drawImage(
            image=self.path_to_brandline_file,
            x=0,  # x (левый край)
            y=0,  # y (нижний край)
            width=_pixels_to_points(pixels=self.brand_line_width_height[0]),
            height=_pixels_to_points(pixels=self.brand_line_width_height[1]),
        )

    def afterPage(self):
        """
        Вызывается каждый раз после обработки каждой страницы
        """

        self._add_brandline(self.canv, self)
