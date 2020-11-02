import os
import sys
from pathlib import Path

from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize


def get_app_icon() -> QIcon:
    """
    Reads icon files of different sizes and convert them to QIcon.

    Returns:
        App icon.
    """

    app_icon = QIcon()
    icon_paths = Path(os.path.join(sys.path[0], "src/gui/res/app_icon"))
    for icon in icon_paths.iterdir():
        app_icon.addFile(str(icon), QSize(int(icon.stem), int(icon.stem)))
    return app_icon


def get_main_qml_path() -> str:
    """Returns path to main GUI file."""

    return os.path.join(sys.path[0], "src/gui/res/layout/main.qml")
