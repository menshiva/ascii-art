from __future__ import annotations
import os
import sys
import time
from threading import Thread, Event
from typing import Callable, Tuple
from pathlib import Path

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtGui import QFontMetrics
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication, QFileDialog

from src.factory import ArtFactory
from src.image import Image
from src.util.consts import uiConsts
from . import res


class Gui(QObject):
    artFactory: ArtFactory
    __imageThreadSignal: Signal = Signal(int)
    __animationThreadSignal: Signal = Signal(int)
    __animationThread: Thread
    __animationStopEvent: Event

    __app: QApplication
    __engine: QQmlApplicationEngine
    __open_file_dialog: QFileDialog
    __root: QObject
    __settings: QObject
    __artLayout: QObject
    __artList: QObject
    __artSizeSlider: QObject
    __playAnimBtn: QObject
    __stopAnimBtn: QObject
    imageDialog: QObject

    on_open_art_dialog: Callable[[Gui, int], None]
    on_preview_art: Callable[[Gui, Image], None]
    on_image_processed: Callable[[Gui, int], None]
    on_add_edit_art: Callable[[Gui, int, str], None]
    on_draw_art: Callable[[Gui, int], None]
    on_remove_art: Callable[[Gui, int], None]
    on_apply_grayscale: Callable[[Gui, str], None]

    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.artFactory = art_factory
        # noinspection PyUnresolvedReferences
        self.__imageThreadSignal.connect(self.__on_image_processed)
        # noinspection PyUnresolvedReferences
        self.__animationThreadSignal.connect(self.__art_list_change_index)

        os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QQuickStyle.setStyle("Material")
        self.__app = QApplication(sys.argv)
        self.__app.setApplicationName(uiConsts["ProjectName"])
        self.__app.setOrganizationName(uiConsts["AuthorName"])
        self.__app.setOrganizationDomain(uiConsts["ProjectDomain"])
        self.__app.setWindowIcon(res.get_app_icon())

        self.__engine = QQmlApplicationEngine()
        self.__engine.rootContext().setContextProperty("Consts", uiConsts)
        self.__engine.rootContext().setContextProperty("Gui", self)
        self.__engine.rootContext().setContextProperty(
            "ArtFactory", self.artFactory
        )
        self.__engine.load(res.get_main_qml_path())

        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__root = self.__engine.rootObjects()[0]
        self.__settings = self.__root.findChild(QObject, "settings")
        self.__artLayout = self.__root.findChild(QObject, "artLayout")
        self.__artList = self.__root.findChild(QObject, "artList")
        self.__artSizeSlider = self.__root.findChild(QObject, "artSizeSlider")
        self.__playAnimBtn = self.__root.findChild(QObject, "playAnimBtn")
        self.__stopAnimBtn = self.__root.findChild(QObject, "stopAnimBtn")
        self.imageDialog = self.__root.findChild(QObject, "imageDialog")

        self.__artList.currentItemChanged.connect(self.__draw_art)
        self.__init_animation_thread()
        self.__init_open_file_dialog()

    def __del__(self) -> None:
        Path(os.path.join(sys.path[0], "tmp.ppm")).unlink(True)
        try:
            self.__artList.currentItemChanged.disconnect(self.__draw_art)
        except RuntimeError:
            pass

    def process_image_background(self, index: int, image: Image) -> None:
        self.artFactory.loaded_image = image
        Thread(target=self.__image_processing_thread, args=(
            index, image, self.__imageThreadSignal
        )).start()

    def compute_art_label_size(self) -> Tuple[int, int]:
        art_width = int(self.__get_property(
            self.__artLayout, "width"
        ).read())
        art_height = int(self.__get_property(
            self.__artLayout, "height"
        ).read())
        fm = QFontMetrics(
            self.__get_property(self.__artLayout, "font").read()
        )
        char_width = art_width // fm.averageCharWidth()
        char_height = art_height // fm.height()
        return char_width, char_height

    def print_art(self, art: str) -> None:
        self.__get_property(self.__artLayout, "text").write(art)

    def set_play_animation_button_enable(self, enable: bool) -> None:
        self.__get_property(self.__playAnimBtn, "enabled").write(enable)

    def get_current_art_list_index(self) -> int:
        return int(self.__get_property(self.__artList, "currentIndex").read())

    def exec(self) -> None:
        sys.exit(self.__app.exec_())

    @Slot(int)
    def __open_art_dialog(self, index: int) -> None:
        self.on_open_art_dialog(self, index)

    @Slot(str, str, bool, bool, bool, bool, str)
    def __preview_art(self, name: str, path: str,
                      contrast: bool, negative: bool,
                      convolution: bool, emboss: bool,
                      grayscale: str) -> None:
        self.on_preview_art(self, Image(
            name, path,
            contrast, negative,
            convolution, emboss,
            grayscale
        ))

    @Slot(int)
    def __on_image_processed(self, index: int) -> None:
        self.on_image_processed(self, index)

    @Slot(int, str)
    def __add_edit_art(self, index: int, name: str) -> None:
        self.on_add_edit_art(self, index, name)

    @Slot()
    def __draw_art(self) -> None:
        self.on_draw_art(self, self.get_current_art_list_index())

    @Slot(int)
    def __remove_art(self, index: int) -> None:
        self.on_remove_art(self, index)

    @Slot(str)
    def __apply_grayscale(self, new_grayscale: str) -> None:
        self.on_apply_grayscale(self, new_grayscale)

    # noinspection PyTypeChecker
    @Slot(result=str)
    def __browse_files(self) -> str:
        if self.__open_file_dialog.exec_():
            selected_files = self.__open_file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]
        return ""

    @Slot()
    def __start_animation(self) -> None:
        self.__get_property(self.__artSizeSlider, "enabled").write(False)
        self.__get_property(self.__playAnimBtn, "enabled").write(False)
        self.__get_property(self.__stopAnimBtn, "enabled").write(True)
        self.__init_animation_thread()
        self.__animationThread.start()

    @Slot()
    def __stop_animation(self) -> None:
        if self.__animationThread and self.__animationThread.is_alive():
            self.__animationStopEvent.set()
            self.__animationThread.join()
            self.__get_property(self.__artSizeSlider, "enabled").write(True)
            self.__get_property(self.__playAnimBtn, "enabled").write(True)
            self.__get_property(self.__stopAnimBtn, "enabled").write(False)

    @Slot(int)
    def __export_art(self, index: int) -> None:
        files = QFileDialog.getSaveFileName(
            caption="Save art",
            filter="Text files (*.txt)"
        )
        if files and files[0]:
            f = open(files[0], "w+")
            # noinspection PyTypeChecker
            f.write(str(self.artFactory[index]))
            f.close()

    @Slot(int)
    def __art_list_change_index(self, index: int) -> None:
        self.__get_property(
            self.__artList, "currentIndex"
        ).write(index)

    def __init_open_file_dialog(self) -> None:
        self.__open_file_dialog = QFileDialog()
        self.__open_file_dialog.setWindowTitle("Open image")
        self.__open_file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.__open_file_dialog.setNameFilter(
            f"Images ({uiConsts['SupportedImageFormats']})"
        )

    def __init_animation_thread(self) -> None:
        duration = float(self.__get_property(
            self.__settings, "animationDuration"
        ).read())
        self.__animationStopEvent = Event()
        self.__animationThread = Thread(target=self.__animation_thread, args=(
            len(self.artFactory), duration,
            self.__animationThreadSignal, self.__animationStopEvent
        ))

    @staticmethod
    def __animation_thread(factory_size: int, duration: float,
                           signal: Signal[int], stop_event: Event) -> None:
        while True:
            for i in range(factory_size - 1, -1, -1):
                if stop_event.is_set():
                    return
                signal.emit(i)
                time.sleep(duration)

    @staticmethod
    def __image_processing_thread(index: int, image: Image,
                                  signal: Signal[int]) -> None:
        image.convert_to_ascii_art()
        signal.emit(index)

    @staticmethod
    def __get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)
