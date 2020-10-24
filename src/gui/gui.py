from __future__ import annotations
import os
import sys
import time
from threading import Thread, Event
from typing import Callable, Tuple

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtGui import QFontMetrics
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication, QFileDialog

from src.factory.art_factory import ArtFactory
from src.gui.res import layout
from src.image.image import Image
from src.util.consts import uiConsts


class Gui(QObject):
    artFactory: ArtFactory
    __imgThreadSignal: Signal = Signal(int, Image)
    __animationThreadSignal: Signal = Signal(int)
    __animationThread: Thread
    __animationStopEvent: Event

    __app: QApplication
    __engine: QQmlApplicationEngine
    __open_img_dialog: QFileDialog
    __root: QObject
    __settings: QObject
    __artLayout: QObject
    __artList: QObject
    __artSizeSlider: QObject
    __playAnimBtn: QObject
    __stopAnimBtn: QObject
    addImageDialog: QObject

    onAddEditArtCallback: Callable[[Gui, int, Image], None]
    onImageProcessed: Callable[[Gui, int, Image], None]
    onRemoveArtCallback: Callable[[Gui, int], None]
    onOpenArtDialogCallback: Callable[[Gui, int], None]
    onDrawArtCallback: Callable[[Gui, int], None]
    onApplyGrayscale: Callable[[Gui, str], None]

    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.artFactory = art_factory
        # noinspection PyUnresolvedReferences
        self.__imgThreadSignal.connect(self.__on_image_processed)
        # noinspection PyUnresolvedReferences
        self.__animationThreadSignal.connect(self.__art_list_change_index)

        os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QQuickStyle.setStyle("Material")
        self.__app = QApplication(sys.argv)
        self.__app.setApplicationName(uiConsts["ProjectName"])
        self.__app.setOrganizationName(uiConsts["AuthorName"])
        self.__app.setOrganizationDomain(uiConsts["AuthorEmail"])

        self.__engine = QQmlApplicationEngine()
        self.__engine.rootContext().setContextProperty("Consts", uiConsts)
        self.__engine.rootContext().setContextProperty("Gui", self)
        self.__engine.rootContext().setContextProperty(
            "ArtFactory", self.artFactory
        )
        self.__engine.load(layout.get_main_qml())

        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__root = self.__engine.rootObjects()[0]
        self.__settings = self.__root.findChild(QObject, "settings")
        self.__artLayout = self.__root.findChild(QObject, "artLayout")
        self.__artList = self.__root.findChild(QObject, "artList")
        self.__artSizeSlider = self.__root.findChild(QObject, "artSizeSlider")
        self.__playAnimBtn = self.__root.findChild(QObject, "playAnimBtn")
        self.__stopAnimBtn = self.__root.findChild(QObject, "stopAnimBtn")
        self.addImageDialog = self.__root.findChild(QObject, "addImageDialog")

        self.__artList.currentItemChanged.connect(self.__draw_art)
        self.__init_animation_thread()
        self.__init_open_img_dialog()

    def __del__(self) -> None:
        try:
            self.__artList.currentItemChanged.disconnect(self.__draw_art)
        except RuntimeError:
            pass

    def process_image_background(self, index: int, img: Image) -> None:
        Thread(target=self.__image_processing_thread, args=(
            index, img, self.__imgThreadSignal
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

    @Slot(int, str, str, bool, bool, bool, str)
    def __add_edit_art(self, index: int, name: str, path: str,
                       contrast: bool, negative: bool, convolution: bool,
                       grayscale: str) -> None:
        self.onAddEditArtCallback(
            self,
            index,
            Image(name, path, contrast, negative, convolution, grayscale)
        )

    @Slot(int, Image)
    def __on_image_processed(self, index: int, img: Image) -> None:
        self.onImageProcessed(self, index, img)

    @Slot(int)
    def __remove_art(self, index: int) -> None:
        self.onRemoveArtCallback(self, index)

    @Slot(int)
    def __open_art_dialog(self, index: int) -> None:
        self.onOpenArtDialogCallback(self, index)

    @Slot()
    def __draw_art(self) -> None:
        index = int(self.__get_property(self.__artList, "currentIndex").read())
        self.onDrawArtCallback(self, index)

    @Slot(str)
    def __apply_grayscale(self, new_grayscale: str) -> None:
        self.onApplyGrayscale(self, new_grayscale)

    # noinspection PyTypeChecker
    @Slot(result=str)
    def __browse_files(self) -> str:
        if self.__open_img_dialog.exec_():
            selected_files = self.__open_img_dialog.selectedFiles()
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
            f.write(self.artFactory[index].export_art())
            f.close()

    @Slot(int)
    def __art_list_change_index(self, index: int) -> None:
        self.__get_property(
            self.__artList, "currentIndex"
        ).write(index)

    def __init_open_img_dialog(self) -> None:
        self.__open_img_dialog = QFileDialog()
        self.__open_img_dialog.setWindowTitle("Open image")
        self.__open_img_dialog.setFileMode(QFileDialog.ExistingFile)
        self.__open_img_dialog.setNameFilter(
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

    def exec(self) -> None:
        sys.exit(self.__app.exec_())

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
    def __image_processing_thread(index: int, img: Image,
                                  signal: Signal[Image, int]) -> None:
        img.convert_to_ascii_art()
        signal.emit(index, img)

    @staticmethod
    def __get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)
