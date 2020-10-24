from __future__ import annotations
from typing import List, Dict, Final, Iterator

from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex

from src.image.image import Image


class ArtFactory(QAbstractListModel):
    __NAME_ROLE: Final = Qt.DisplayRole
    __IMAGE_ROLE: Final = Qt.DecorationRole
    __CONTRAST_ROLE: Final = Qt.CheckStateRole
    __NEGATIVE_ROLE: Final = Qt.CheckStateRole + 1
    __CONVOLUTION_ROLE: Final = Qt.CheckStateRole + 2
    __arts: List[Image] = []
    lastDrawedArt: int = -1

    def __add__(self, item: Image) -> ArtFactory:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__arts.insert(0, item)
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

    def __iter__(self) -> Iterator[Image]:
        return iter(self.__arts)

    def __contains__(self, index: int) -> bool:
        return len(self.__arts) > index

    def data(self, index, role=Qt.DisplayRole) -> str:
        row = index.row()
        return {
            self.__NAME_ROLE: self.__arts[row].name,
            self.__IMAGE_ROLE: self.__arts[row].path,
            self.__CONTRAST_ROLE: self.__arts[row].is_contrast,
            self.__NEGATIVE_ROLE: self.__arts[row].is_negative,
            self.__CONVOLUTION_ROLE: self.__arts[row].is_convolution,
        }[role]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__arts)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.__NAME_ROLE: b"name",
            self.__IMAGE_ROLE: b"path",
            self.__CONTRAST_ROLE: b"contrast",
            self.__NEGATIVE_ROLE: b"negative",
            self.__CONVOLUTION_ROLE: b"convolution"
        }
