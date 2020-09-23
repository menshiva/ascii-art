import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import Qt
from PySide2.QtQuickControls2 import QQuickStyle
from src.uiConsts import uiConsts

if __name__ == '__main__':
    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QQuickStyle.setStyle("Material")
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("Consts", uiConsts)
    engine.load("src/view.qml")

    sys.exit(app.exec_())
