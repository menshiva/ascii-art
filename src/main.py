from src.gui.Gui import Gui
from src.factory.ArtFactory import ArtFactory
from src.image.Image import Image
from PySide2.QtWidgets import QFileDialog


# TODO
# def func(gui: Gui):
#     art_width = gui.get_property(gui.artLayout, "width").read()
#     art_height = gui.get_property(gui.artLayout, "height").read()
#     fm = QFontMetrics(gui.get_property(gui.artLayout, "font").read())
#
#     char_width = int(art_width / fm.averageCharWidth())
#     char_height = int(art_height / fm.height())
#
#     text = []
#     for h in range(char_height):
#         for w in range(char_width):
#             text.append("s")
#         text.append("\n")
#
#     gui.get_property(gui.artLayout, "text").write("".join(text))


def add_art(gui: Gui, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
    gui.artFactory += Image(name, path, contrast, negative, convolution)


def edit_art(gui: Gui, index: int, name: str, contrast: bool, negative: bool, convolution: bool) -> None:
    gui.artFactory[index] = Image(name, "", contrast, negative, convolution)


def remove_art(gui: Gui, index: int) -> None:
    del gui.artFactory[index]


def open_art_dialog(gui: Gui, index: int) -> None:
    if index == -1:
        gui.addImageDialog.openDialog(-1, "", "", True, False, False)
    else:
        image = gui.artFactory[index]
        gui.addImageDialog.openDialog(
            index, image.name, image.path, image.contrast, image.negative, image.convolution
        )


def browse_art() -> str:
    browse_dialog = QFileDialog()
    browse_dialog.setWindowTitle("Open Image")
    browse_dialog.setFileMode(QFileDialog.ExistingFile)
    browse_dialog.setNameFilter("Images (*.ppm *.jpg)")
    if browse_dialog.exec_():
        selected_files = browse_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
    return ""


def main():
    art_factory = ArtFactory()
    # TODO
    art_factory += Image(
        "vlad", "/run/user/1000/doc/de44aa83/photo_2020-09-27_20-37-29.jpg", False, False, False
    )

    art_factory += Image(
        "misa", "/run/user/1000/doc/45de00f0/photo_2020-09-27_15-32-33.jpg", True, False, True
    )

    art_factory += Image(
        "egor", "/run/user/1000/doc/54ed4330/test2.jpg", True, True, False
    )

    gui = Gui(art_factory)
    gui.onAddArtCallback = add_art
    gui.onEditArtCallback = edit_art
    gui.onRemoveArtCallback = remove_art
    gui.onOpenArtDialogCallback = open_art_dialog
    gui.onBrowseCallback = browse_art
    gui.exec()


if __name__ == '__main__':
    main()
