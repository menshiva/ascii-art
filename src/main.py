import sys
from src.gui.gui import Gui


# TODO
# def func(gui: UI):
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


def main():
    gui = Gui(sys.argv)
    # gui.btn.clicked.connect(lambda: func(gui))  # TODO
    gui.exec()


if __name__ == '__main__':
    main()
