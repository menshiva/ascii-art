from __future__ import annotations
from typing import List, Dict, Final, Iterator

from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex

from src.image import Image


class ArtFactory(QAbstractListModel):
    __NAME_ROLE: Final[int]
    __IMAGE_ROLE: Final[int]
    __arts: List[Image]
    loaded_image: Image or None

    def __init__(self) -> None:
        super().__init__()
        self.__NAME_ROLE = Qt.DisplayRole
        self.__IMAGE_ROLE = Qt.DecorationRole
        self.__arts = []
        self.loaded_image = None

    def __add__(self, new_image: Image) -> ArtFactory:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__arts.insert(0, new_image)
        self.endInsertRows()
        return self

    def __setitem__(self, index: int, new_image: Image) -> None:
        row = self.index(index)
        self.__arts[index] = new_image
        self.dataChanged.emit(row, row, self.roleNames())

    def __getitem__(self, index: int) -> Image:
        return self.__arts[index]

    def __delitem__(self, index: int) -> None:
        self.beginRemoveColumns(QModelIndex(), index, index)
        del self.__arts[index]
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
            self.__IMAGE_ROLE: self.__arts[row].path
        }[role]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__arts)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.__NAME_ROLE: b"name",
            self.__IMAGE_ROLE: b"path"
        }
