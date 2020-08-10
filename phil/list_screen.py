""" List of photos to work on """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableView
from phil.data_context import DataContext
from phil.photo_model import PhotoModel


class ListScreen(QWidget):
    """ The main selection and display screen """

    def __init__(self, data_context: DataContext, parent=None):
        super().__init__(parent)
        self.data_context = data_context
        self.photo_list = QTableView()
        self.photo_list.setModel(self.data_context.photo_model)
        self.photo_list.setEditTriggers(QTableView.NoEditTriggers)
        self.photo_list.setSelectionBehavior(QTableView.SelectRows)
        # self.photo_list.selectionModel().selectionChanged.connect(
        #     self.selection_changed
        # )
        self.photo_list.hideColumn(PhotoModel.Columns.DESCRIPTION)

        layout = QHBoxLayout()
        layout.addWidget(self.photo_list)

        self.setLayout(layout)
