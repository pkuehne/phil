""" Photo details screen """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QDataWidgetMapper
from phil.data_context import DataContext
from phil.photo_model import PhotoModel
from phil.photo_viewer import PhotoViewer
from phil.navigation_buttons import NavigationButtons
from phil.person_linker import PersonLinker
from phil.person_linker import LinkerDelegate


class DetailScreen(QWidget):
    """ Displays details of a photo """

    def __init__(self, data_context: DataContext, parent=None):
        super().__init__(parent)

        self.data_context = data_context
        layout = QVBoxLayout()
        self.photo_viewer = PhotoViewer()
        layout.addWidget(self.photo_viewer)

        form = QFormLayout()
        self.filename = QLabel()
        form.addRow(QLabel("Filename:"), self.filename)
        # self.date_taken = QDateEdit()
        # form.addRow(QLabel("Date Taken:"), self.date_taken)
        self.description = QTextEdit()
        form.addRow(QLabel("Description:"), self.description)

        self.linker = PersonLinker([], self)
        form.addRow(QLabel("People:"), self.linker)

        layout.addLayout(form)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.photo_model)
        self.mapper.setItemDelegate(LinkerDelegate(self))
        self.mapper.addMapping(self.filename, PhotoModel.Columns.FILENAME, b"text")
        # self.mapper.addMapping(self.date_taken, PhotoModel.Columns.DATE_TAKEN)
        self.mapper.addMapping(
            self.description, PhotoModel.Columns.DESCRIPTION, b"plainText"
        )
        self.mapper.addMapping(self.linker, PhotoModel.Columns.PERSONS)

        self.mapper.currentIndexChanged.connect(self.row_changed)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        # self.data_context.photo_model.dataChanged.connect()

        self.navigation_buttons = NavigationButtons(self.mapper)
        layout.addWidget(self.navigation_buttons)
        self.setLayout(layout)

    def row_changed(self, row: int):
        """ The selected photo has changed """
        self.photo_viewer.load_image(
            self.data_context.photo_model.index(row, PhotoModel.Columns.FILEPATH).data()
        )
