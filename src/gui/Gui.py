from __future__ import annotations

import os
import sys
import time
from threading import Thread, Event
from typing import Callable

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication

from src.factory.ArtFactory import ArtFactory
from src.gui.util.GuiConsts import uiConsts
from src.image.Image import Image


class Gui(QObject):
    artFactory: ArtFactory
    __imgThreadSignal: Signal = Signal(Image, int)
    __animationThreadSignal: Signal = Signal(int)
    __animationThread: Thread
    __animationStopEvent: Event

    app: QApplication
    engine: QQmlApplicationEngine
    root: QObject
    settings: QObject
    artLayout: QObject
    artList: QObject
    addImageDialog: QObject
    artSizeSlider: QObject
    playAnimBtn: QObject
    stopAnimBtn: QObject

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
        self.app = QApplication(sys.argv)
        self.app.setOrganizationName("Ivan Menshikov")
        self.app.setOrganizationDomain("menshiva@fit.cvut.cz")
        self.app.setApplicationName("ASCII art")

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("Consts", uiConsts)
        self.engine.rootContext().setContextProperty("Gui", self)
        self.engine.rootContext().setContextProperty("ArtFactory", self.artFactory)
        self.engine.load(f"{os.path.dirname(__file__)}/res/layout/main.qml")

        if not self.engine.rootObjects():
            sys.exit(-1)
        self.__init_views()
        self.__setup_animation_thread()

    def __del__(self) -> None:
        try:
            self.artList.currentItemChanged.disconnect(self.draw_art)
        except RuntimeError:
            pass

    def __init_views(self) -> None:
        self.root = self.engine.rootObjects()[0]
        self.settings = self.root.findChild(QObject, "settings")
        self.artLayout = self.root.findChild(QObject, "artLayout")
        self.artList = self.root.findChild(QObject, "artList")
        self.addImageDialog = self.root.findChild(QObject, "addImageDialog")
        self.artSizeSlider = self.root.findChild(QObject, "artSizeSlider")
        self.playAnimBtn = self.root.findChild(QObject, "playAnimBtn")
        self.stopAnimBtn = self.root.findChild(QObject, "stopAnimBtn")
        self.artList.currentItemChanged.connect(self.draw_art)

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
            for i, _ in enumerate(factory.arts()):
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
        sys.exit(self.app.exec_())
