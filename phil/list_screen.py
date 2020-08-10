""" List of photos to work on """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QHeaderView
from phil.data_context import DataContext
from phil.photo_model import PhotoModel
from phil.detail_screen import DetailScreen


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
        self.photo_list.hideColumn(PhotoModel.Columns.FILEPATH)

        self.photo_list.horizontalHeader().setSectionResizeMode(
            PhotoModel.Columns.FILENAME, QHeaderView.Stretch
        )

        self.detail_screen = DetailScreen(self.data_context)
        self.photo_list.selectionModel().currentRowChanged.connect(
            self.detail_screen.mapper.setCurrentModelIndex
        )

        layout = QHBoxLayout()
        layout.addWidget(self.photo_list)
        layout.addWidget(self.detail_screen)
        self.setLayout(layout)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) < 1:
            return
        index = selected.indexes()[0]
        print(f"{index}")
        self.detail_screen.mapper.setRootIndex(index.parent())
        self.detail_screen.mapper.setCurrentModelIndex(index)
