from __future__ import annotations
from typing import List, Dict, Final
from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex
from src.image.Image import Image


class ArtFactory(QAbstractListModel):
    NAME_ROLE: Final = Qt.DisplayRole
    IMAGE_ROLE: Final = Qt.DecorationRole
    CONTRAST_ROLE: Final = Qt.CheckStateRole
    NEGATIVE_ROLE: Final = Qt.CheckStateRole + 1
    CONVOLUTION_ROLE: Final = Qt.CheckStateRole + 2
    __arts: List[Image]
    lastDrawedArt: int

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.lastDrawedArt = -1
        self.__arts = []

    def __add__(self, value: Image) -> ArtFactory:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__arts.insert(0, value)
        self.endInsertRows()
        return self

    def __setitem__(self, key: int, new_img: Image) -> None:
        row = self.index(key)
        self.__arts[key] = new_img
        self.dataChanged.emit(row, row, self.roleNames())

    def __getitem__(self, key: int) -> Image:
        return self.__arts[key]

    def __delitem__(self, key: int) -> None:
        self.beginRemoveColumns(QModelIndex(), key, key)
        del self.__arts[key]
        self.endRemoveRows()

    def __len__(self) -> int:
        return len(self.__arts)

    def arts(self) -> List[Image]:
        return self.__arts

    def is_exist(self, index: int) -> bool:
        return len(self.__arts) > index

    def data(self, index, role=Qt.DisplayRole) -> str:
        row = index.row()
        return {
            self.NAME_ROLE: self.__arts[row].name,
            self.IMAGE_ROLE: self.__arts[row].path,
            self.CONTRAST_ROLE: self.__arts[row].is_contrast,
            self.NEGATIVE_ROLE: self.__arts[row].is_negative,
            self.CONVOLUTION_ROLE: self.__arts[row].is_convolution,
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
