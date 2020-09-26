import sys
from src.gui.gui import Gui


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
    gui.artModels.add_person("sosi zopu")


def main():
    gui = Gui(sys.argv)
    gui.addImageBtn.clicked.connect(lambda: add_art(gui))
    gui.exec()


if __name__ == '__main__':
    main()
