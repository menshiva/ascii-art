from __future__ import annotations
import os
import sys
import time
from threading import Thread, Event
from typing import Callable, Tuple
from pathlib import Path

from PySide2.QtCore import Qt, QObject, Slot, Signal
from PySide2.QtGui import QFontMetrics
from PySide2.QtQml import QQmlApplicationEngine, QQmlProperty
from PySide2.QtQuickControls2 import QQuickStyle
from PySide2.QtWidgets import QApplication, QFileDialog

from src.factory import ArtFactory
from src.image import Image
from src.util.consts import uiConsts
from . import res


class Gui(QObject):
    art_factory: ArtFactory
    __image_thread_signal: Signal = Signal(int)
    __animation_thread_signal: Signal = Signal(int)
    __animation_thread: Thread
    __animation_stop_event: Event

    __app: QApplication
    __engine: QQmlApplicationEngine
    __open_file_dialog: QFileDialog
    __root: QObject
    __settings: QObject
    __art_layout: QObject
    __art_list: QObject
    __art_size_slider: QObject
    __play_anim_button: QObject
    __stop_anim_Button: QObject
    image_dialog: QObject

    on_open_art_dialog: Callable[[Gui, int], None]
    on_preview_art: Callable[[Gui, Image], None]
    on_image_processed: Callable[[Gui, int], None]
    on_add_edit_art: Callable[[Gui, int, str], None]
    on_draw_art: Callable[[Gui, int], None]
    on_remove_art: Callable[[Gui, int], None]
    on_apply_grayscale: Callable[[Gui, str], None]

    def __init__(self, art_factory: ArtFactory) -> None:
        super().__init__()
        self.art_factory = art_factory
        # noinspection PyUnresolvedReferences
        self.__image_thread_signal.connect(self.__on_image_processed)
        # noinspection PyUnresolvedReferences
        self.__animation_thread_signal.connect(self.__art_list_change_index)

        os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
        QApplication.setAttribute(Qt.AA_PluginApplication)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QQuickStyle.setStyle("Material")
        self.__app = QApplication(sys.argv)
        self.__app.setApplicationName(uiConsts["ProjectName"])
        self.__app.setOrganizationName(uiConsts["AuthorName"])
        self.__app.setOrganizationDomain(uiConsts["ProjectDomain"])
        self.__app.setWindowIcon(res.get_app_icon())

        self.__engine = QQmlApplicationEngine()
        self.__engine.rootContext().setContextProperty("Consts", uiConsts)
        self.__engine.rootContext().setContextProperty("Gui", self)
        self.__engine.rootContext().setContextProperty(
            "ArtFactory", self.art_factory
        )
        self.__engine.load(res.get_main_qml_path())

        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__root = self.__engine.rootObjects()[0]
        self.__settings = self.__root.findChild(QObject, "settings")
        self.__art_layout = self.__root.findChild(QObject, "artLayout")
        self.__art_list = self.__root.findChild(QObject, "artList")
        self.__art_size_slider = self.__root.findChild(
            QObject, "artSizeSlider"
        )
        self.__play_anim_button = self.__root.findChild(QObject, "playAnimBtn")
        self.__stop_anim_Button = self.__root.findChild(QObject, "stopAnimBtn")
        self.image_dialog = self.__root.findChild(QObject, "imageDialog")

        self.__art_list.currentItemChanged.connect(self.__draw_art)
        self.__init_animation_thread()
        self.__init_open_file_dialog()

    def __del__(self) -> None:
        Path(os.path.join(sys.path[0], "tmp.ppm")).unlink(True)
        self.__stop_animation()
        self.__art_list.currentItemChanged.disconnect(self.__draw_art)
        self.__app.quit()

    def process_image_background(self, index: int, image: Image) -> None:
        Thread(target=self.__image_thread_func, args=(
            index, image, self.__image_thread_signal
        )).start()

    def compute_art_layout_size(self) -> Tuple[int, int]:
        art_width = int(self.__get_property(
            self.__art_layout, "width"
        ).read())
        art_height = int(self.__get_property(
            self.__art_layout, "height"
        ).read())
        fm = QFontMetrics(
            self.__get_property(self.__art_layout, "font").read()
        )
        char_width = art_width // fm.averageCharWidth()
        char_height = art_height // fm.height()
        return char_width, char_height

    def print_art(self, art: str) -> None:
        self.__get_property(self.__art_layout, "text").write(art)

    def set_play_animation_button_enable(self, enable: bool) -> None:
        self.__get_property(self.__play_anim_button, "enabled").write(enable)

    def get_current_art_list_index(self) -> int:
        return int(self.__get_property(self.__art_list, "currentIndex").read())

    def show(self) -> None:
        sys.exit(self.__app.exec_())

    @Slot(int)
    def __open_art_dialog(self, index: int) -> None:
        self.on_open_art_dialog(self, index)

    @Slot(str, str, bool, bool, bool, bool, str)
    def __preview_art(self, name: str, path: str,
                      contrast: bool, negative: bool,
                      convolution: bool, emboss: bool,
                      grayscale: str) -> None:
        self.on_preview_art(self, Image(
            name, path,
            contrast, negative,
            convolution, emboss,
            grayscale
        ))

    @Slot(int)
    def __on_image_processed(self, index: int) -> None:
        self.on_image_processed(self, index)

    @Slot(int, str)
    def __add_edit_art(self, index: int, name: str) -> None:
        self.on_add_edit_art(self, index, name)

    @Slot()
    def __draw_art(self) -> None:
        self.on_draw_art(self, self.get_current_art_list_index())

    @Slot(int)
    def __remove_art(self, index: int) -> None:
        self.on_remove_art(self, index)

    @Slot(str)
    def __apply_grayscale(self, new_grayscale: str) -> None:
        self.on_apply_grayscale(self, new_grayscale)

    # noinspection PyTypeChecker
    @Slot(result=str)
    def __browse_files(self) -> str:
        if self.__open_file_dialog.exec_():
            selected_files = self.__open_file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]
        return ""

    @Slot()
    def __start_animation(self) -> None:
        self.__get_property(self.__art_size_slider, "enabled").write(False)
        self.__get_property(self.__play_anim_button, "enabled").write(False)
        self.__get_property(self.__stop_anim_Button, "enabled").write(True)
        self.__init_animation_thread()
        self.__animation_thread.start()

    @Slot()
    def __stop_animation(self) -> None:
        if self.__animation_thread and self.__animation_thread.is_alive():
            self.__animation_stop_event.set()
            self.__animation_thread.join()
            self.__get_property(
                self.__art_size_slider, "enabled"
            ).write(True)
            self.__get_property(
                self.__play_anim_button, "enabled"
            ).write(True)
            self.__get_property(
                self.__stop_anim_Button, "enabled"
            ).write(False)

    @Slot(int)
    def __export_art(self, index: int) -> None:
        files = QFileDialog.getSaveFileName(
            caption="Save art",
            filter="Text files (*.txt)"
        )
        if files and files[0]:
            f = open(files[0], "w+")
            f.write(str(self.art_factory[index]))
            f.close()

    @Slot(int)
    def __art_list_change_index(self, index: int) -> None:
        self.__get_property(
            self.__art_list, "currentIndex"
        ).write(index)

    def __init_open_file_dialog(self) -> None:
        self.__open_file_dialog = QFileDialog()
        self.__open_file_dialog.setWindowTitle("Open image")
        self.__open_file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.__open_file_dialog.setNameFilter(
            f"Images ({uiConsts['SupportedImageFormats']})"
        )

    def __init_animation_thread(self) -> None:
        duration = float(self.__get_property(
            self.__settings, "animationDuration"
        ).read())
        self.__animation_stop_event = Event()
        self.__animation_thread = Thread(
            target=self.__animation_thread_func,
            args=(
                len(self.art_factory), duration,
                self.__animation_thread_signal, self.__animation_stop_event
            )
        )

    @staticmethod
    def __animation_thread_func(factory_size: int,
                                duration: float,
                                signal: Signal[int],
                                stop_event: Event) -> None:
        while True:
            for i in range(factory_size - 1, -1, -1):
                if stop_event.is_set():
                    return
                signal.emit(i)
                time.sleep(duration)

    @staticmethod
    def __image_thread_func(index: int, image: Image,
                            signal: Signal[int]) -> None:
        image.convert_to_ascii_art()
        signal.emit(index)

    @staticmethod
    def __get_property(element: QObject, prop: str) -> QQmlProperty:
        return QQmlProperty(element, prop)
