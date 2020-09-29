from typing import List, Dict, Final
from src.image.Image import Image
from PySide2.QtCore import Qt, QAbstractListModel, Slot, QModelIndex


class ArtFactory(QAbstractListModel):
    NAME_ROLE: Final = Qt.DisplayRole
    IMAGE_ROLE: Final = Qt.DecorationRole
    CONTRAST_ROLE: Final = Qt.CheckStateRole
    NEGATIVE_ROLE: Final = Qt.CheckStateRole + 1
    CONVOLUTION_ROLE: Final = Qt.CheckStateRole + 2
    __arts: List[Image]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.__arts = []

    def data(self, index, role=Qt.DisplayRole) -> str:
        row = index.row()
        return {
            self.NAME_ROLE: self.__arts[row].name,
            self.IMAGE_ROLE: self.__arts[row].path,
            self.CONTRAST_ROLE: self.__arts[row].contrast,
            self.NEGATIVE_ROLE: self.__arts[row].negative,
            self.CONVOLUTION_ROLE: self.__arts[row].convolution,
        }[role]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__arts)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.NAME_ROLE: b"name",
            self.IMAGE_ROLE: b"path",
            self.CONTRAST_ROLE: b"contrast",
            self.NEGATIVE_ROLE: b"negative",
            self.CONVOLUTION_ROLE: b"convolution"
        }

    @Slot(str, str, bool, bool, bool)
    def add_art(self, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__arts.insert(0, Image(name, path, contrast, negative, convolution))
        self.endInsertRows()

    @Slot(int, str, bool, bool, bool)
    def edit_art(self, row: int, name: str, contrast: bool, negative: bool, convolution: bool) -> None:
        ix = self.index(row)
        self.__arts[row].apply_changes(name, contrast, negative, convolution)
        self.dataChanged.emit(ix, ix, self.roleNames())

    @Slot(int)
    def remove_art(self, row: int) -> None:
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self.__arts[row]
        self.endRemoveRows()
