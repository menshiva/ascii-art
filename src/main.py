from src.gui.Gui import Gui
from src.factory.ArtFactory import ArtFactory


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


def browse_art(gui: Gui) -> None:
    gui.get_property(gui.addImageDialogPathBox, "text").write(gui.browse_files())


# TODO
# def display_art(gui: Gui):
#     current_item = gui.get_property(gui.artList, "currentIndex").read()
#     print(current_item)


def main():
    art_factory = ArtFactory()
    art_factory.add_art(
        "vlad", "/run/user/1000/doc/de44aa83/photo_2020-09-27_20-37-29.jpg", False, False, False
    )
    art_factory.add_art(
        "misa", "/run/user/1000/doc/45de00f0/photo_2020-09-27_15-32-33.jpg", True, False, True
    )
    art_factory.add_art(
        "egor", "/run/user/1000/doc/54ed4330/test2.jpg", True, True, False
    )

    gui = Gui(art_factory)
    gui.addImageDialogBrowseBtn.clicked.connect(lambda: browse_art(gui))
    # gui.artList.currentItemChanged.connect(lambda: display_art(gui))
    gui.exec()


if __name__ == '__main__':
    main()
