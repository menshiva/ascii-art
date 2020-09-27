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
        self.arts = []

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

    def add_art(self, art: Image) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.arts.insert(0, art)
        self.endInsertRows()

    def edit_art(self, row: int, art: Image) -> None:
        ix = self.index(row)
        self.arts[row] = art
        self.dataChanged.emit(ix, ix, self.roleNames())

    @Slot(int)
    def delete_art(self, row: int) -> None:
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.arts[row]
        self.endRemoveRows()
