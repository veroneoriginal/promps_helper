# pylint: disable=E0611: no-name-in-module
import sys
from typing import Callable

from PyQt6.QtGui import (
    QTextCursor,
    QGuiApplication,
)
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import (
    QThread,
    pyqtSignal,
    QObject,
)

from PyQt6.QtWidgets import QProgressBar

from control_manager.main import ControlManager
from ga_parser.main import start_parser
from source.structure_for_products import PARAMETERS_DIF_PRODUCT_CATEGORIES

FILE_PATH_TOOLS = '00_base/Средства_АКТУАЛЬНАЯ.xlsx'
FILE_PATH_COLLECTION = '00_base/Подборки_мои.xlsx'
PATH_TO_OUTPUT_FOLDER = '00_base/00_info_for_post'


class EmittingStream(QObject):
    """
    Кастомный поток для перехвата print.
    Этот поток подменяет sys.stdout внутри потока выполнения в
    FunctionWorkerThread.run()
    """
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass


class FunctionWorkerThread(QThread):
    """
    Универсальный класс для потока.
    Передаём нужный объект и вызываем с нужными аргументами
    внутри потока.
    Вывод всех принтов идёт в UI.
    """
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)

    def __init__(self, target: Callable, *args, **kwargs):
        """
        Объект для запуска логики в потоке
        """
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Запуск потока
        """
        stream = EmittingStream()
        stream.text_written.connect(self.log_signal.emit)
        sys.stdout = stream

        try:
            def update_progress(current, total):
                self.progress_signal.emit(current, total)

            self.kwargs['progress_callback'] = update_progress
            self.target(*self.args, **self.kwargs)

        # pylint: disable=W0718 broad-exception-caught
        except Exception as e:
            self.log_signal.emit(f"❌ Ошибка: {e}\n")
        finally:
            sys.stdout = sys.__stdout__


# pylint: disable=R0902: too-many-instance-attributes
class MainWindow(QWidget):
    """
    Главное окно UI
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генерация подборок")
        self.setGeometry(100, 100, 600, 400)
        self.center_on_screen()

        layout = QVBoxLayout()

        # Кнопка "Спарсить средства"
        self.button_parse = QPushButton("🎬 Спарсить средства")
        self.button_parse.clicked.connect(self.start_parse)
        layout.addWidget(self.button_parse)

        # Кнопка "Создать подборку"
        self.button_generate = QPushButton("🔥 Генерировать подборки")
        self.button_generate.clicked.connect(self.start_create_collection)
        layout.addWidget(self.button_generate)

        # Кнопка "Перегенерировать PDF и посты"
        self.button_pdf = QPushButton("🔃 Перегенерировать PDF и посты")
        self.button_pdf.clicked.connect(self.start_recreate_pdf)
        layout.addWidget(self.button_pdf)

        # Кнопка "Очистить лог"
        self.button_clear_log = QPushButton("🧹 Очистить лог")
        self.button_clear_log.clicked.connect(self.clear_log)
        layout.addWidget(self.button_clear_log)

        # Прогресс бар
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        self.progress_bar.setValue(0)

        # Окно для лога
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        layout.addWidget(self.text_log)

        self.setLayout(layout)

        self.worker_collection = None
        self.worker_pdf = None

    def clear_log(self):
        """
        Очистка окна лога
        """
        self.text_log.clear()

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def update_progress(self, current, total):
        """
        Метод обновления прогресс-бара
        """
        if total > 0:
            percent = int((current / total) * 100)
            self.progress_bar.setValue(percent)

    def start_worker(self, target_func: Callable, log_message: str, *args, **kwargs):
        """
        Запуск воркера
        """
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        self.text_log.append(log_message)
        self.on_process_start()

        worker = FunctionWorkerThread(target_func, *args, **kwargs)
        worker.log_signal.connect(self.append_log)
        worker.progress_signal.connect(self.update_progress)
        worker.finished.connect(self.on_process_finished)
        worker.start()

        return worker

    def start_create_collection(self):
        """
        Запуск создания подборок
        """
        self.worker_collection = self.start_worker(
            ControlManager(PARAMETERS_DIF_PRODUCT_CATEGORIES).create_collection,
            "▶️ Запуск генерации подборок...\n",
            file_path_tools=FILE_PATH_TOOLS,
            file_path_collection=FILE_PATH_COLLECTION,
            path_to_output_folder=PATH_TO_OUTPUT_FOLDER
        )

    def start_recreate_pdf(self):
        """
        Запуск перегенерации постов и PDF
        """
        self.worker_pdf = self.start_worker(
            ControlManager(PARAMETERS_DIF_PRODUCT_CATEGORIES).recreate_pdf_and_posts,
            "▶️ Запуск перегенерации PDF и постов...\n",
            file_path_tools=FILE_PATH_TOOLS,
            file_path_collection=FILE_PATH_COLLECTION,
            path_to_output_folder=PATH_TO_OUTPUT_FOLDER
        )

    def start_parse(self):
        """
        Запуск Парсера
        """
        self.worker_parse = self.start_worker(
            start_parser,
            "▶️ Запуск парсера...\n",
            table_path=FILE_PATH_TOOLS,
            ws_title='Средства',
            image_dir_path='00_base/products/00_img',
            base_delay=3
        )

    def append_log(self, text: str) -> None:
        """
        Добавление записи в лог
        """
        self.text_log.moveCursor(QTextCursor.MoveOperation.End)
        self.text_log.insertPlainText(text)

    def on_process_finished(self) -> None:
        """
        Завершение процесса - разблокирование кнопок
        """
        self.text_log.append("\n✅ Работа завершена.")
        self.button_parse.setEnabled(True)
        self.button_pdf.setEnabled(True)
        self.button_generate.setEnabled(True)
        self.button_clear_log.setEnabled(True)

    def on_process_start(self):
        """
        Старт процесса - блокирование кнопок
        """
        self.button_parse.setEnabled(False)
        self.button_pdf.setEnabled(False)
        self.button_generate.setEnabled(False)
        self.button_clear_log.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
