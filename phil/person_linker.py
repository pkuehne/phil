""" Widget to handle Person links to Photos """

from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QItemDelegate
from PyQt5.QtWidgets import QDataWidgetMapper
from phil.photo import Person
from phil.person_model import PersonModel
from phil.photo_model import PhotoModel


class LinkerDelegate(QItemDelegate):
    """ Delegate to correctly pass data to PersonLinker """

    def setEditorData(self, widget, index):  # pylint: disable=invalid-name, no-self-use
        """ Set data on widget from index """
        if index.column() == PhotoModel.Columns.PERSONS:
            widget.set_persons(index.data(Qt.EditRole))

    def setModelData(
        self, widget, model, index
    ):  # pylint: disable=invalid-name, no-self-use
        """ Set data on widget from index """
        if index.column() == PhotoModel.Columns.PERSONS:
            model.setData(index, widget.get_persons())


class PersonLinker(QWidget):
    """ Displays details of a photo """

    def __init__(self, persons: List[Person], parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()

        self.model = PersonModel(persons)
        self.person_list = QTableView()
        self.person_list.setModel(self.model)
        self.person_list.setEditTriggers(QTableView.NoEditTriggers)
        self.person_list.setSelectionBehavior(QTableView.SelectRows)
        self.person_list.horizontalHeader().setSectionResizeMode(
            PersonModel.Columns.NAME, QHeaderView.Stretch
        )

        layout.addWidget(self.person_list)

        edit_layout = QVBoxLayout()
        self.name = QLineEdit()
        edit_layout.addWidget(self.name)
        edit_layout.addStretch()

        button_layout = QHBoxLayout()
        self.add = QPushButton("Add")
        self.add.pressed.connect(self.model.add_person)
        button_layout.addWidget(self.add)
        self.delete = QPushButton("Delete")
        button_layout.addWidget(self.delete)
        edit_layout.addLayout(button_layout)
        layout.addLayout(edit_layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.name, PersonModel.Columns.NAME)
        self.person_list.selectionModel().currentRowChanged.connect(
            self.mapper.setCurrentModelIndex
        )
        self.delete.pressed.connect(
            lambda: self.model.delete_person(
                self.model.index(self.mapper.currentIndex(), 0)
            )
        )

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def get_persons(self):
        """Get the persons from the model """
        return self.person_list.model().get_person_list()

    def set_persons(self, persons: List[Person]):
        """ Sets the persons on the model """
        self.person_list.model().set_person_list(persons)
