import os
import sys
from typing import List
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtCore import Qt, QObject
from PySide2.QtQuickControls2 import QQuickStyle
from src.ui.util.uiConsts import uiConsts


class UI:
    app: QGuiApplication
    engine: QQmlApplicationEngine
    artLayout: QObject

    def __init__(self, argv: List[str]) -> None:
        super().__init__()
        os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
        QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QQuickStyle.setStyle("Material")
        self.app = QGuiApplication(argv)

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("Consts", uiConsts)
        self.engine.load(f"{os.path.dirname(__file__)}/res/layout/main.qml")
        # engine.load("qml/main.qml") # TODO

        if not self.engine.rootObjects():
            sys.exit(-1)
        self.__init_views()

    def __init_views(self) -> None:
        root = self.engine.rootObjects()[0]
        self.artLayout = root.findChild(QObject, "artLayout")

    @staticmethod
    def get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)

    def exec(self) -> None:
        sys.exit(self.app.exec_())
