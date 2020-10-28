import os
import sys
from pathlib import Path

from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize


def get_app_icon() -> QIcon:
    app_icon = QIcon()
    icon_paths = Path(
        os.path.join(sys.path[0], "src/gui/res/app_icon")
    ).glob("*")
    for icon in icon_paths:
        app_icon.addFile(str(icon), QSize(int(icon.stem), int(icon.stem)))
    return app_icon


def get_main_qml_path() -> str:
    return os.path.join(sys.path[0], "src/gui/res/layout/main.qml")