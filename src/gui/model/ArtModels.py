from typing import List, Dict
from src.image.Image import Image
from PySide2.QtCore import Qt, QAbstractListModel, Slot, QModelIndex


class ArtModels(QAbstractListModel):
    textRole: int
    imgRole: int
    arts: List[Image]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.textRole = Qt.DisplayRole
        self.imgRole = Qt.DecorationRole
        self.arts = [  # TODO
            Image("vlad lox", "/run/user/1000/doc/de44aa83/photo_2020-09-27_20-37-29.jpg"),
            Image("misa", "/run/user/1000/doc/45de00f0/photo_2020-09-27_15-32-33.jpg"),
            Image("egor huj s gor", "/run/user/1000/doc/54ed4330/test2.jpg")
        ]

    def data(self, index, role=Qt.DisplayRole) -> str:
        row = index.row()
        if role == self.textRole:
            return self.arts[row].name
        if role == self.imgRole:
            return self.arts[row].path

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.arts)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.textRole: b"name",
            self.imgRole: b"path"
        }

    # TODO effects
    @Slot(str, str, bool, bool, bool)
    def add_art(self, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.arts.insert(0, Image(name, path))
        self.endInsertRows()

    # TODO effects
    @Slot(int, str, str, bool, bool, bool)
    def edit_art(self, row: int, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
        ix = self.index(row)
        self.arts[row] = Image(name, path)
        self.dataChanged.emit(ix, ix, self.roleNames())

    @Slot(int)
    def delete_art(self, row: int) -> None:
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.arts[row]
        self.endRemoveRows()
