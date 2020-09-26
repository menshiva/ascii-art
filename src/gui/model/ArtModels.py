from typing import List
from PySide2.QtCore import Qt, QAbstractListModel, Slot, QModelIndex


class ArtModels(QAbstractListModel):
    # arts  TODO
    nameRole: int

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nameRole = Qt.UserRole + 1
        self.arts = []

    def data(self, index, role=Qt.DisplayRole) -> str:
        row = index.row()
        if role == self.nameRole:
            return self.arts[row]["name"]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.arts)

    def roleNames(self):
        return {
            self.nameRole: b"name"
        }

    @Slot(str, int)
    def add_person(self, name: str) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.arts.insert(0, {"name": name})
        self.endInsertRows()

    @Slot(int, str, int)
    def edit_person(self, row: int, name: str) -> None:
        ix = self.index(row)
        self.arts[row] = {"name": name}
        self.dataChanged.emit(ix, ix, self.roleNames())

    @Slot(int)
    def delete_person(self, row: int) -> None:
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.arts[row]
        self.endRemoveRows()
