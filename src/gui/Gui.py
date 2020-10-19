from __future__ import annotations
from typing import Callable

import os
import sys
import time
from threading import Thread, Event

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication

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
    settings: QObject
    artLayout: QObject
    artList: QObject
    addImageDialog: QObject
    artSizeSlider: QObject
    playAnimBtn: QObject

    onAddArtCallback: Callable[[Gui, str, str, str, bool, bool, bool], None]
    onEditArtCallback: Callable[[Gui, int, str, str, bool, bool, bool], None]
    onImageLoaded: Callable[[Gui, Image, int], None]
    onRemoveArtCallback: Callable[[Gui, int], None]
    onOpenArtDialogCallback: Callable[[Gui, int], None]
    onBrowseArtCallback: Callable[[], str]
    onDrawArtCallback: Callable[[Gui, int], None]
    onArtSizeChanged: Callable[[Gui, int], None]
    onApplyGrayscale: Callable[[Gui, str], None]
    onExportArt: Callable[[Gui, int], None]

    # noinspection PyUnresolvedReferences
    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.artFactory = art_factory
        self.__imgThreadSignal.connect(self.on_image_loaded)
        self.__animationThreadSignal.connect(self.art_list_change_index)

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
        self.settings = self.__root.findChild(QObject, "settings")
        self.artLayout = self.__root.findChild(QObject, "artLayout")
        self.artList = self.__root.findChild(QObject, "artList")
        self.addImageDialog = self.__root.findChild(QObject, "addImageDialog")
        self.artSizeSlider = self.__root.findChild(QObject, "artSizeSlider")
        self.playAnimBtn = self.__root.findChild(QObject, "playAnimBtn")
        self.artList.currentItemChanged.connect(self.draw_art)

        self.__setup_animation_thread()

    def __del__(self) -> None:
        try:
            self.artList.currentItemChanged.disconnect(self.draw_art)
        except RuntimeError:
            pass

    @Slot(str, str, str, bool, bool, bool)
    def add_art(self,
                name: str, path: str, grayscale: str,
                contrast: bool, negative: bool, convolution: bool) -> None:
        self.onAddArtCallback(self, name, path, grayscale, contrast, negative, convolution)

    @Slot(int, str, str, bool, bool, bool)
    def edit_art(self, index: int,
                 name: str, grayscale: str,
                 contrast: bool, negative: bool, convolution: bool) -> None:
        self.onEditArtCallback(self, index, name, grayscale, contrast, negative, convolution)

    @Slot(int)
    def remove_art(self, index: int) -> None:
        self.onRemoveArtCallback(self, index)

    @Slot(int)
    def open_art_dialog(self, index: int) -> None:
        self.onOpenArtDialogCallback(self, index)

    @Slot(result=str)
    def browse_files(self) -> str:
        return self.onBrowseArtCallback()

    @Slot()
    def draw_art(self) -> None:
        index: int = self.get_property(self.artList, "currentIndex").read()
        self.onDrawArtCallback(self, index)

    @Slot(int)
    def change_art_size(self, value: int) -> None:
        self.onArtSizeChanged(self, value)

    @Slot(str)
    def apply_grayscale(self, grayscale: str) -> None:
        self.onApplyGrayscale(self, grayscale)

    @Slot()
    def start_animation(self) -> None:
        self.get_property(self.artSizeSlider, "enabled").write(False)
        self.get_property(self.playAnimBtn, "enabled").write(False)
        self.get_property(self.stopAnimBtn, "enabled").write(True)
        self.__setup_animation_thread()
        self.__animationThread.start()

    @Slot()
    def stop_animation(self) -> None:
        if self.__animationThread and self.__animationThread.is_alive():
            self.__animationStopEvent.set()
            self.__animationThread.join()
            self.get_property(self.artSizeSlider, "enabled").write(True)
            self.get_property(self.playAnimBtn, "enabled").write(True)
            self.get_property(self.stopAnimBtn, "enabled").write(False)

    def load_image(self, index: int,
                   name: str, path: str, grayscale: str,
                   contrast: bool, negative: bool, convolution: bool) -> None:
        Thread(target=self.__img_thread, args=(
            name, path, grayscale,
            contrast, negative, convolution,
            index, self.__imgThreadSignal
        )).start()

    @Slot(int)
    def export_art(self, index: int) -> None:
        self.onExportArt(self, index)

    @Slot(int)
    def art_list_change_index(self, index: int) -> None:
        self.get_property(self.artList, "currentIndex").write(index)

    @Slot(Image, int)
    def on_image_loaded(self, img: Image, index: int):
        self.onImageLoaded(self, img, index)

    def __setup_animation_thread(self) -> None:
        duration: float = self.get_property(self.settings, "animationDuration").read()
        self.__animationStopEvent = Event()
        self.__animationThread = Thread(target=self.__animation_thread, args=(
            self.artFactory, duration,
            self.__animationThreadSignal, self.__animationStopEvent
        ))

    @staticmethod
    def __animation_thread(factory: ArtFactory, duration: float,
                           signal: Signal[int], stop_event: Event) -> None:
        while True:
            for i, _ in enumerate(factory):
                if stop_event.is_set():
                    return
                signal.emit(i)
                time.sleep(duration)

    @staticmethod
    def __img_thread(name: str, path: str, grayscale: str,
                     contrast: bool, negative: bool, convolution: bool,
                     index: int, signal: Signal[Image, int]) -> None:
        signal.emit(Image(name, path, grayscale, contrast, negative, convolution), index)

    @staticmethod
    def get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)

    def exec(self) -> None:
        sys.exit(self.__app.exec_())
