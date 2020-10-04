from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QFontMetrics
from src.gui.Gui import Gui
from src.factory.ArtFactory import ArtFactory
from src.image.Image import Image


def add_art(gui: Gui,
            name: str, path: str, grayscale: str,
            contrast: bool, negative: bool, convolution: bool) -> None:
    gui.artFactory.lastDrawedArt += 1
    gui.artFactory += Image(name, path, grayscale, contrast, negative, convolution)
    if len(gui.artFactory) > 1:
        gui.get_property(gui.playAnimBtn, "enabled").write(True)


def edit_art(gui: Gui, index: int,
             name: str, grayscale: str,
             contrast: bool, negative: bool, convolution: bool) -> None:
    old_img = gui.artFactory[index]
    gui.artFactory[index] = Image(name, old_img.path, grayscale, contrast, negative, convolution)
    if gui.artFactory.lastDrawedArt == index:
        draw_art(gui, index)


def remove_art(gui: Gui, index: int) -> None:
    if index < gui.artFactory.lastDrawedArt:
        gui.artFactory.lastDrawedArt -= 1
    del gui.artFactory[index]
    if len(gui.artFactory) < 2:
        gui.get_property(gui.playAnimBtn, "enabled").write(False)


def open_art_dialog(gui: Gui, index: int) -> None:
    if index == -1:
        gui.addImageDialog.openDialog(-1, "", "", True, False, False)
    else:
        image = gui.artFactory[index]
        gui.addImageDialog.openDialog(
            index, image.name, image.path, image.is_contrast, image.is_negative, image.is_convolution
        )


def browse_art() -> str:
    browse_dialog = QFileDialog()
    browse_dialog.setWindowTitle("Open Image")
    browse_dialog.setFileMode(QFileDialog.ExistingFile)
    browse_dialog.setNameFilter("Images (*.pgm *.ppm *.jpg *.jpeg *.png)")
    if browse_dialog.exec_():
        selected_files = browse_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
    return ""


def draw_art(gui: Gui, index: int) -> None:
    if not gui.artFactory.is_exist(index):
        gui.artFactory.lastDrawedArt = -1
        gui.get_property(gui.artLayout, "text").write("")
        return
    gui.artFactory.lastDrawedArt = index
    art_width: int = gui.get_property(gui.artLayout, "width").read()
    art_height: int = gui.get_property(gui.artLayout, "height").read()
    fm: QFontMetrics = QFontMetrics(gui.get_property(gui.artLayout, "font").read())
    char_width: int = art_width // fm.averageCharWidth()
    char_height: int = art_height // fm.height()
    art: str = gui.artFactory[index].get_ascii_art(char_width, char_height)
    gui.get_property(gui.artLayout, "text").write(art)


def change_art_size(gui: Gui, value: int) -> None:
    gui.get_property(gui.artLayout, "font.pixelSize").write(value)
    if gui.artFactory.lastDrawedArt != -1:
        draw_art(gui, gui.artFactory.lastDrawedArt)


def apply_grayscale(gui: Gui, grayscale: str) -> None:
    for i, art in enumerate(gui.artFactory.arts()):
        edit_art(gui, i, art.name, grayscale, art.is_contrast, art.is_negative, art.is_convolution)


def main():
    art_factory = ArtFactory()
    gui = Gui(art_factory)
    gui.onAddArtCallback = add_art
    gui.onEditArtCallback = edit_art
    gui.onRemoveArtCallback = remove_art
    gui.onOpenArtDialogCallback = open_art_dialog
    gui.onBrowseCallback = browse_art
    gui.onDrawArtCallback = draw_art
    gui.onArtSizeChanged = change_art_size
    gui.onApplyGrayscale = apply_grayscale
    gui.exec()


if __name__ == '__main__':
    main()
