from __future__ import annotations
from typing import List, Dict, Final, Iterator

from PySide2.QtCore import Qt, QAbstractListModel, QModelIndex

from src.image import Image


class ArtFactory(QAbstractListModel):
    """
    Image controller.

    This is a general factory class for images.
    Stores and controls all loaded images (add, update, remove, count etc.).
    Manages the connection between main program logic, loaded images and GUI.
    Inherits QAbstractListModel class for connection with GUI.

    Attributes:
        __NAME_ROLE: Final[int]
            Private constant for defining a name of the image.
        __IMAGE_ROLE: Final[int]
            Private constant for defining a path of the image.
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
        """Factory initialization."""

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
                Image to be added.

        Returns:
            ArtFactory instance.
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
                Index of the image to get.

        Returns:
            Image at the given index.
        """

        return self.__arts[index]

    def __delitem__(self, index: int) -> None:
        """
        x.__delitem__(y) <==> del x[y]

        Args:
            index: int
                Index of the image to remove.

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
            Total number of added images.
        """

        return len(self.__arts)

    def __iter__(self) -> Iterator[Image]:
        """
        x.__iter__() <==> iter(x)

        Returns:
            Iterator for all the added images.
        """

        return iter(self.__arts)

    def __contains__(self, index: int) -> bool:
        """
        if x.__contains__(y) <==> if y in x

        Args:
            index: int
                Index to check.

        Returns:
            If image exists at the given index.
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
            Data taken from given role and index of the item.
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
            A dictionary mapping image attributes to the corresponding roles.
        """

        return {
            self.__NAME_ROLE: b"name",
            self.__IMAGE_ROLE: b"path"
        }
