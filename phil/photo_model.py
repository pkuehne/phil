""" The PhotoModel contains all the basic data about the photos """

from typing import List
from enum import IntEnum, unique
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from phil.photo import Photo


class PhotoModel(QAbstractTableModel):
    """ Model representation of Photos """

    @unique
    class Columns(IntEnum):
        """ Enum for the Model columns """

        FILENAME = 0
        PATH = 1
        FILEPATH = 2
        HASH = 3
        DATE_TAKEN = 4
        DESCRIPTION = 5

    def __init__(self, photos: List[Photo] = None):
        super().__init__()
        self.photos: List[Photo] = photos if photos else []

    def update_photo_list(self, photos: List[Photo]):
        """ Update the list of photos """
        self.beginResetModel()
        self.photos = photos
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):  # pylint: disable=invalid-name
        """ Number of individuals """
        if parent.isValid():
            return 0
        return len(self.photos)

    def columnCount(
        self, parent=QModelIndex()
    ):  # pylint: disable=invalid-name, no-self-use
        """ Columns in the model """
        if parent.isValid():
            return 0
        return len(list(self.Columns))

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """ Get individual for a row/column """
        if not index.isValid() or role not in [
            Qt.DisplayRole,
            Qt.ToolTipRole,
            Qt.EditRole,
        ]:
            return None
        photo = self.photos[index.row()]

        return {
            self.Columns.HASH: photo.hash,
            self.Columns.FILENAME: photo.filename,
            self.Columns.PATH: photo.path,
            self.Columns.FILEPATH: photo.filepath,
            self.Columns.DATE_TAKEN: photo.date_taken,
            self.Columns.DESCRIPTION: photo.description,
        }[index.column()]

    def headerData(
        self, section, orientation, role
    ):  # pylint: disable=invalid-name, no-self-use
        """ Set the header information """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return {
                self.Columns.HASH: "Unique ID",
                self.Columns.FILENAME: "Filename",
                self.Columns.PATH: "Path",
                self.Columns.FILEPATH: "File Path",
                self.Columns.DATE_TAKEN: "Date Taken",
                self.Columns.DESCRIPTION: "Description",
            }.get(section, "")
        return None

    # def flags(self, index):  # pylint: disable= no-self-use
    #     """ Returns the flags for the given index """
    #     if not index.isValid():
    #         return Qt.NoItemFlags
    #     flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
    #     flags |= {
    #         self.Columns.HASH: Qt.NoItemFlags,
    #         self.Columns.FILENAME: Qt.NoItemFlags,
    #         self.Columns.PATH: Qt.NoItemFlags,
    #     }.get(index.column(), Qt.ItemIsEditable)
    #     return flags
