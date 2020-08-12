""" The PersonModel contains all the basic data about the persons """

from typing import List
from enum import IntEnum, unique
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from phil.photo import Person


class PersonModel(QAbstractTableModel):
    """ Model representation of Persons """

    @unique
    class Columns(IntEnum):
        """ Enum for the Model columns """

        NAME = 0

    def __init__(self, persons: List[Person] = None):
        super().__init__()
        self.persons: List[Person] = persons if persons else []

    def set_person_list(self, persons: List[Person]):
        """ Update the list of persons """
        self.beginResetModel()
        self.persons = persons
        self.endResetModel()

    def get_person_list(self):
        """ Returns the list of persons """
        return self.persons

    def add_person(self):
        """ Add a new person """
        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(QModelIndex(), len(self.persons), len(self.persons))

        self.persons.append(Person())

        self.endInsertRows()
        self.layoutChanged.emit()

    def delete_person(self, index):
        """ Deletes the node at the given index """
        if not index.isValid():
            return
        self.beginRemoveRows(index.parent(), index.row(), index.row())

        del self.persons[index.row()]

        self.endRemoveRows()

    def rowCount(self, parent=QModelIndex()):  # pylint: disable=invalid-name
        """ Number of individuals """
        if parent.isValid():
            return 0
        return len(self.persons)

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
            Qt.EditRole,
        ]:
            return None
        person = self.persons[index.row()]

        return {
            Qt.DisplayRole: self.data_display,
            Qt.ToolTipRole: self.data_display,
            Qt.EditRole: self.data_edit,
        }[role](person, index.column())

    def data_display(self, person: Person, column: int):
        """ Get the data for a person field """
        return {self.Columns.NAME: person.name,}[column]

    def data_edit(self, person: Person, column: int):
        """ Get the edit representation for a person field """
        return {self.Columns.NAME: person.name,}[column]

    def setData(self, index, value, role=Qt.EditRole):  # pylint: disable=invalid-name
        """ Updates the nodes values based on an edit """
        if (
            not index.isValid()
            or index.column() > self.columnCount()
            or role != Qt.EditRole
        ):
            return False
        prev = ""

        person = self.persons[index.row()]
        if index.column() == self.Columns.NAME:
            prev = person.name
            person.name = value

        if prev != value:
            self.dataChanged.emit(index, index)
        return True

    def headerData(
        self, section, orientation, role
    ):  # pylint: disable=invalid-name, no-self-use
        """ Set the header information """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return {self.Columns.NAME: "People in Photo",}.get(section, "")
        return None
