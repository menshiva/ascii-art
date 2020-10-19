from __future__ import annotations
from typing import Callable, Tuple

import os
import sys
import time
from threading import Thread, Event

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication, QFileDialog
from PySide2.QtGui import QFontMetrics

from src.gui.res import layout
from src.factory.ArtFactory import ArtFactory
from src.image.Image import Image
from src.util.Consts import uiConsts


class Gui(QObject):
    artFactory: ArtFactory
    __imgThreadSignal: Signal = Signal(Image, int)
    __animationThreadSignal: Signal = Signal(int)
    __animationThread: Thread
    __animationStopEvent: Event

    __app: QApplication
    __engine: QQmlApplicationEngine
    __root: QObject
    __settings: QObject
    __artLayout: QObject
    __artList: QObject
    __artSizeSlider: QObject
    __playAnimBtn: QObject
    __stopAnimBtn: QObject
    addImageDialog: QObject

    onAddArtCallback: Callable[[Gui, str, str, str, bool, bool, bool], None]
    onEditArtCallback: Callable[[Gui, int, str, str, bool, bool, bool], None]
    onImageProcessed: Callable[[Gui, Image, int], None]
    onRemoveArtCallback: Callable[[Gui, int], None]
    onOpenArtDialogCallback: Callable[[Gui, int], None]
    onDrawArtCallback: Callable[[Gui, int], None]
    onApplyGrayscale: Callable[[Gui, str], None]

    # noinspection PyUnresolvedReferences
    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.artFactory = art_factory
        self.__imgThreadSignal.connect(self.__on_image_processed)
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
        self.__engine.rootContext().setContextProperty("ArtFactory", self.artFactory)
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
        self.__setup_animation_thread()

    def __del__(self) -> None:
        try:
            self.__artList.currentItemChanged.disconnect(self.__draw_art)
        except RuntimeError:
            pass

    @Slot(str, str, str, bool, bool, bool)
    def __add_art(self,
                  name: str, path: str, grayscale: str,
                  contrast: bool, negative: bool, convolution: bool) -> None:
        self.onAddArtCallback(self, name, path, grayscale, contrast, negative, convolution)

    @Slot(int, str, str, bool, bool, bool)
    def __edit_art(self, index: int,
                   name: str, grayscale: str,
                   contrast: bool, negative: bool, convolution: bool) -> None:
        self.onEditArtCallback(self, index, name, grayscale, contrast, negative, convolution)

    @Slot(Image, int)
    def __on_image_processed(self, img: Image, index: int):
        self.onImageProcessed(self, img, index)

    @Slot(int)
    def __remove_art(self, index: int) -> None:
        self.onRemoveArtCallback(self, index)

    @Slot(int)
    def __open_art_dialog(self, index: int) -> None:
        self.onOpenArtDialogCallback(self, index)

    @Slot()
    def __draw_art(self) -> None:
        index: int = self.__get_property(self.__artList, "currentIndex").read()
        self.onDrawArtCallback(self, index)

    @Slot(str)
    def __apply_grayscale(self, grayscale: str) -> None:
        self.onApplyGrayscale(self, grayscale)

    @Slot(result=str)
    def __browse_files(self) -> str:
        browse_dialog = QFileDialog()
        browse_dialog.setWindowTitle("Open image")
        browse_dialog.setFileMode(QFileDialog.ExistingFile)
        browse_dialog.setNameFilter("Images (*.pgm *.ppm *.jpg *.jpeg *.png)")
        if browse_dialog.exec_():
            selected_files = browse_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]
        return ""

    @Slot()
    def __start_animation(self) -> None:
        self.__get_property(self.__artSizeSlider, "enabled").write(False)
        self.__get_property(self.__playAnimBtn, "enabled").write(False)
        self.__get_property(self.__stopAnimBtn, "enabled").write(True)
        self.__setup_animation_thread()
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
        files = QFileDialog.getSaveFileName(caption="Save art", filter="Text files (*.txt)")
        if files and files[0]:
            f = open(files[0], "w+")
            f.write(self.artFactory[index].export_art())
            f.close()

    @Slot(int)
    def __art_list_change_index(self, index: int) -> None:
        self.__get_property(self.__artList, "currentIndex").write(index)
            
    def process_image_background(self, index: int,
                                 name: str, path: str, grayscale: str,
                                 contrast: bool, negative: bool, convolution: bool) -> None:
        Thread(target=self.__image_processing_thread, args=(
            name, path, grayscale,
            contrast, negative, convolution,
            index, self.__imgThreadSignal
        )).start()

    def compute_art_label_size(self) -> Tuple[int, int]:
        art_width: int = self.__get_property(self.__artLayout, "width").read()
        art_height: int = self.__get_property(self.__artLayout, "height").read()
        fm: QFontMetrics = QFontMetrics(self.__get_property(self.__artLayout, "font").read())
        char_width: int = art_width // fm.averageCharWidth()
        char_height: int = art_height // fm.height()
        return char_width, char_height

    def print_art(self, art: str) -> None:
        self.__get_property(self.__artLayout, "text").write(art)

    def set_play_animation_button_enable(self, enable: bool) -> None:
        self.__get_property(self.__playAnimBtn, "enabled").write(enable)

    def __setup_animation_thread(self) -> None:
        duration: float = self.__get_property(self.__settings, "animationDuration").read()
        self.__animationStopEvent = Event()
        self.__animationThread = Thread(target=self.__animation_thread, args=(
            self.artFactory, duration,
            self.__animationThreadSignal, self.__animationStopEvent
        ))

    def exec(self) -> None:
        sys.exit(self.__app.exec_())

    @staticmethod
    def __animation_thread(factory: ArtFactory, duration: float,
                           signal: Signal[int], stop_event: Event) -> None:
        while True:
            for i in range(len(factory) - 1, -1, -1):
                if stop_event.is_set():
                    return
                signal.emit(i)
                time.sleep(duration)

    @staticmethod
    def __image_processing_thread(name: str, path: str, grayscale: str,
                                  contrast: bool, negative: bool, convolution: bool,
                                  index: int, signal: Signal[Image, int]) -> None:
        signal.emit(Image(name, path, grayscale, contrast, negative, convolution), index)

    @staticmethod
    def __get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)
