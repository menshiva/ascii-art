from __future__ import annotations
import os
import sys
from typing import Callable
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtCore import Qt, QObject, Slot
from PySide2.QtQuickControls2 import QQuickStyle
from src.gui.util.GuiConsts import uiConsts
from src.factory.ArtFactory import ArtFactory


class Gui(QObject):
    artFactory: ArtFactory

    app: QApplication
    engine: QQmlApplicationEngine
    root: QObject
    settings: QObject
    artLayout: QObject
    artList: QObject
    addImageDialog: QObject
    playAnimBtn: QObject
    stopAnimBtn: QObject

    onAddArtCallback: Callable[[Gui, str, str, bool, bool, bool], None]
    onEditArtCallback: Callable[[Gui, int, str, bool, bool, bool], None]
    onRemoveArtCallback: Callable[[Gui, int], None]
    onOpenArtDialogCallback: Callable[[Gui, int], None]
    onBrowseCallback: Callable[[], str]
    onDrawArtCallback: Callable[[Gui, int], None]
    onArtSizeChanged: Callable[[Gui, int], None]
    onApplySettings: Callable[[Gui], None]

    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.artFactory = art_factory

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
        # self.engine.load("qml/main.qml")  # TODO

        if not self.engine.rootObjects():
            sys.exit(-1)
        self.__init_views()

    def __del__(self) -> None:
        self.artList.currentItemChanged.disconnect(self.draw_art)

    def __init_views(self) -> None:
        self.root = self.engine.rootObjects()[0]
        self.settings = self.root.findChild(QObject, "settings")
        self.artLayout = self.root.findChild(QObject, "artLayout")
        self.artList = self.root.findChild(QObject, "artList")
        self.addImageDialog = self.root.findChild(QObject, "addImageDialog")
        self.playAnimBtn = self.root.findChild(QObject, "playAnimBtn")
        self.stopAnimBtn = self.root.findChild(QObject, "stopAnimBtn")
        self.artList.currentItemChanged.connect(self.draw_art)

    @Slot(str, str, bool, bool, bool)
    def add_art(self, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.onAddArtCallback(self, name, path, contrast, negative, convolution)

    @Slot(int, str, bool, bool, bool)
    def edit_art(self, index: int, name: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.onEditArtCallback(self, index, name, contrast, negative, convolution)

    @Slot(int)
    def remove_art(self, index: int) -> None:
        self.onRemoveArtCallback(self, index)

    @Slot(int)
    def open_art_dialog(self, index: int) -> None:
        self.onOpenArtDialogCallback(self, index)

    @Slot(result=str)
    def browse_files(self) -> str:
        return self.onBrowseCallback()

    @Slot()
    def draw_art(self) -> None:
        index: int = self.get_property(self.artList, "currentIndex").read()
        self.onDrawArtCallback(self, index)

    @Slot(int)
    def change_art_size(self, value: int) -> None:
        self.onArtSizeChanged(self, value)

    @Slot()
    def apply_settings(self) -> None:
        self.onApplySettings(self)

    @staticmethod
    def get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)

    def exec(self) -> None:
        sys.exit(self.app.exec_())
