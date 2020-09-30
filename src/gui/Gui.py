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
    addImageDialog: QObject

    onAddArtCallback: Callable[[Gui, str, str, bool, bool, bool], None]
    onEditArtCallback: Callable[[Gui, int, str, bool, bool, bool], None]
    onRemoveArtCallback: Callable[[Gui, int], None]
    onOpenArtDialogCallback: Callable[[Gui, int], None]
    onBrowseCallback: Callable[[], str]

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

    def __init_views(self) -> None:
        self.root = self.engine.rootObjects()[0]
        self.addImageDialog = self.root.findChild(QObject, "addImageDialog")

    @Slot(str, str, bool, bool, bool)
    def add_art(self, name: str, path: str, contrast: bool, negative: bool, convolution: bool):
        self.onAddArtCallback(self, name, path, contrast, negative, convolution)

    @Slot(int, str, bool, bool, bool)
    def edit_art(self, index: int, name: str, contrast: bool, negative: bool, convolution: bool):
        self.onEditArtCallback(self, index, name, contrast, negative, convolution)

    @Slot(int)
    def remove_art(self, index: int):
        self.onRemoveArtCallback(self, index)

    @Slot(int)
    def open_art_dialog(self, index: int):
        self.onOpenArtDialogCallback(self, index)

    @Slot(result=str)
    def browse_files(self) -> str:
        return self.onBrowseCallback()

    @staticmethod
    def get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)

    def exec(self) -> None:
        sys.exit(self.app.exec_())
