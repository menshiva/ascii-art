from src.gui.Gui import Gui
from src.image.Image import Image


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


def add_art(gui: Gui) -> None:
    art_name = gui.get_property(gui.addImageDialogNameBox, "text").read()
    art_path = gui.get_property(gui.addImageDialogPathBox, "text").read()
    gui.artModels.add_art(Image(art_name, art_path))
    gui.get_property(gui.addImageDialogNameBox, "text").write("")
    gui.get_property(gui.addImageDialogPathBox, "text").write("")


def browse_art(gui: Gui) -> None:
    file_path: str = gui.browse_files()
    gui.get_property(gui.addImageDialogPathBox, "text").write(file_path)


def main():
    gui = Gui()
    gui.addImageBtn.clicked.connect(lambda: add_art(gui))
    gui.addImageDialogBrowseBtn.clicked.connect(lambda: browse_art(gui))
    gui.exec()


if __name__ == '__main__':
    main()
