import sys
from src.ui.ui import UI

# TODO
# def func(user_interface: UI):
#    width = user_interface.get_property("txt", "width").read()
#    print(width)


if __name__ == '__main__':
    ui = UI(sys.argv)

    # TODO
    # button = ui.find_view("btn")
    # button.clicked.connect(lambda: func(ui))
    # width = QQmlProperty(txt, "width").read()
    # print(width)
    # fm = QFontMetrics(QQmlProperty(txt, "font").read())
    # print(group_width / fm.averageCharWidth())

    ui.exec()
