import sys
from src.ui.ui import UI

# TODO
# def func(user_interface: UI):
#     art_width = user_interface.get_property(ui.artLayout, "width").read()
#     art_height = user_interface.get_property(ui.artLayout, "height").read()
#     fm = QFontMetrics(user_interface.get_property(ui.artLayout, "font").read())
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
#     user_interface.get_property(ui.artLayout, "text").write("".join(text))


def main():
    ui = UI(sys.argv)
    # ui.btn.clicked.connect(lambda: func(ui)) # TODO
    ui.exec()


if __name__ == '__main__':
    main()
