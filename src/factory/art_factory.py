from __future__ import annotations
from typing import List, Dict, Final, Iterator

from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex

from src.image import Image


class ArtFactory(QAbstractListModel):
    """
    Image controller.

    This is a general factory class for images.
    Stores all loaded images and can control
    (add, update, remove, count etc.) them.
    Manages connection between main program logic, loaded images and GUI.
    Inherits QAbstractListModel class for connection with GUI.

    Attributes:
        __NAME_ROLE: Final[int]
            Private constant for defining image's name attribute for GUI.
        __IMAGE_ROLE: Final[int]
            Private constant for defining image's path attribute for GUI.
        __arts: List[Image]
            All loaded images.
        loaded_image: Image or None
            Currently adding (but not added yet) image.
    """

    __NAME_ROLE: Final[int]
    __IMAGE_ROLE: Final[int]
    __arts: List[Image]
    loaded_image: Image or None

    def __init__(self) -> None:
        """Inits ArtFactory."""

        super().__init__()
        self.__NAME_ROLE = Qt.DisplayRole
        self.__IMAGE_ROLE = Qt.DecorationRole
        self.__arts = []
        self.loaded_image = None

    def __add__(self, new_image: Image) -> ArtFactory:
        """
        x.__add__(y) <==> x += y

        Args:
            new_image: Image
                New image to add.

        Returns:
            Current ArtFactory instance.
        """

        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__arts.insert(0, new_image)
        self.endInsertRows()
        return self

    def __setitem__(self, index: int, image: Image) -> None:
        """
        x.__setitem_(y, z) <==> x[y] = z

        Args:
            index: int
                Image index.
            image: Image
                Updated image.

        Returns:
            None.
        """

        row = self.index(index)
        self.__arts[index] = image
        self.dataChanged.emit(row, row, self.roleNames())

    def __getitem__(self, index: int) -> Image:
        """
        x.__getitem__(y) <==> x[y]

        Args:
            index: int
                Index of image to get.

        Returns:
            Image at index.
        """

        return self.__arts[index]

    def __delitem__(self, index: int) -> None:
        """
        x.__delitem__(y) <==> del x[y]

        Args:
            index: int
                Index of image to remove.

        Returns:
            None.
        """

        self.beginRemoveColumns(QModelIndex(), index, index)
        del self.__arts[index]
        self.endRemoveRows()

    def __len__(self) -> int:
        """
        x.__len__() <==> len(x)

        Returns:
            Number of added images.
        """

        return len(self.__arts)

    def __iter__(self) -> Iterator[Image]:
        """
        x.__iter__() <==> iter(x)

        Returns:
            Iterator of all added images.
        """

        return iter(self.__arts)

    def __contains__(self, index: int) -> bool:
        """
        if x.__contains__(y) <==> if y in x

        Args:
            index: int
                Index to check.

        Returns:
            If image at index exists.
        """

        return len(self.__arts) > index

    def data(self, index, role=Qt.DisplayRole) -> str:
        """
        Redefined method from QAbstractListModel.

        Args:
            index:
                List item's index.
            role:
                List item's role.

        Returns:
            Data stored under the role for the item by the index.
        """

        row = index.row()
        return {
            self.__NAME_ROLE: self.__arts[row].name,
            self.__IMAGE_ROLE: self.__arts[row].path
        }[role]

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Redefined method from QAbstractListModel.

        Args:
            parent:
                List row's parent.

        Returns:
            Number of rows under the given parent.
        """

        return len(self.__arts)

    def roleNames(self) -> Dict[int, bytes]:
        """
        Redefined method from QAbstractListModel.

        Returns:
            A dict mapping image attributes to the corresponding roles.
        """

        return {
            self.__NAME_ROLE: b"name",
            self.__IMAGE_ROLE: b"path"
        }
