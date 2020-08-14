""" List of photos to work on """

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QHeaderView
from phil.data_context import DataContext
from phil.photo_model import PhotoModel
from phil.detail_screen import DetailScreen
from phil.filter_model import FilterModel


class ListScreen(QWidget):
    """ The main selection and display screen """

    def __init__(self, data_context: DataContext, parent=None):
        super().__init__(parent)
        self.data_context = data_context
        self.filter_model = FilterModel()
        self.filter_model.setSourceModel(self.data_context.photo_model)
        self.photo_list = QTableView()
        self.photo_list.setModel(self.filter_model)
        self.photo_list.setEditTriggers(QTableView.NoEditTriggers)
        self.photo_list.setSelectionBehavior(QTableView.SelectRows)
        self.photo_list.hideColumn(PhotoModel.Columns.DATE_TAKEN)
        self.photo_list.hideColumn(PhotoModel.Columns.DESCRIPTION)
        self.photo_list.hideColumn(PhotoModel.Columns.FILEPATH)

        self.photo_list.horizontalHeader().setSectionResizeMode(
            PhotoModel.Columns.FILENAME, QHeaderView.Stretch
        )

        self.detail_screen = DetailScreen(self.data_context)
        self.photo_list.selectionModel().currentRowChanged.connect(
            self.update_details_screen
        )
        self.detail_screen.mapper.currentIndexChanged.connect(self.update_selection)

        layout = QHBoxLayout()
        layout.addWidget(self.photo_list)
        layout.addWidget(self.detail_screen)
        self.setLayout(layout)

    def update_details_screen(self, index):
        """ update the mapper on the details screen with the new index """
        self.detail_screen.mapper.setCurrentModelIndex(
            self.filter_model.mapToSource(index)
        )

    def update_selection(self, row: int):
        """ Update the selection when the mapper moves """
        index = self.data_context.photo_model.index(row, 0)
        if not self.photo_list.selectionModel().isSelected(index):
            self.photo_list.selectionModel().select(
                index, QItemSelectionModel.ClearAndSelect
            )
