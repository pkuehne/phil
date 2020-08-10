""" Photo details screen """

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImageReader
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDataWidgetMapper
from phil.data_context import DataContext
from phil.photo_model import PhotoModel


class DetailScreen(QWidget):
    """ Displays details of a photo """

    def __init__(self, data_context: DataContext, parent=None):
        super().__init__(parent)

        self.data_context = data_context
        self.scale_factor = 1.0
        layout = QVBoxLayout()

        self.photo = QLabel()
        self.photo.setScaledContents(True)
        self.photo.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.photo)
        layout.addWidget(self.scroll_area)

        image_controls = QHBoxLayout()
        image_controls.addStretch()
        self.size_label = QLabel("100%")
        image_controls.addWidget(QLabel("Zoom:"))
        image_controls.addWidget(self.size_label)
        self.zoom_out = QPushButton("-")
        self.zoom_out.pressed.connect(lambda: self.scale_image(0.8))
        image_controls.addWidget(self.zoom_out)
        self.zoom_zero = QPushButton("Original")
        self.zoom_zero.pressed.connect(self.reset_zoom)
        image_controls.addWidget(self.zoom_zero)
        self.zoom_fit = QPushButton("Fit")
        self.zoom_fit.pressed.connect(self.fit_image)
        image_controls.addWidget(self.zoom_fit)
        self.zoom_in = QPushButton("+")
        self.zoom_in.pressed.connect(lambda: self.scale_image(1.25))
        image_controls.addWidget(self.zoom_in)
        self.reset_zoom()

        layout.addLayout(image_controls)

        form = QFormLayout()
        self.filename = QLabel()
        form.addRow(QLabel("Filename:"), self.filename)
        self.date_taken = QLineEdit()
        form.addRow(QLabel("Date Taken:"), self.date_taken)
        self.description = QTextEdit()
        form.addRow(QLabel("Description"), self.description)

        layout.addLayout(form)
        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.photo_model)
        self.mapper.addMapping(self.filename, PhotoModel.Columns.FILENAME, b"text")
        self.mapper.addMapping(self.date_taken, PhotoModel.Columns.DATE_TAKEN)
        self.mapper.addMapping(
            self.description, PhotoModel.Columns.DESCRIPTION, b"plainText"
        )

        self.mapper.currentIndexChanged.connect(self.row_changed)
        self.data_context.photo_model.dataChanged.connect(
            lambda _, __: self.mapper.toFirst()
        )

    def row_changed(self, row: int):
        """ The selected photo has changed """
        reader = QImageReader(
            self.data_context.photo_model.index(row, PhotoModel.Columns.FILEPATH).data()
        )
        reader.setAutoTransform(True)
        image = reader.read()
        if image is None:
            print("Couldn't load image")
            return
        self.photo.setPixmap(QPixmap.fromImage(image))
        self.fit_image()

    def scale_image(self, factor: float):
        """ Scale the image by the factor """

        self.scale_factor *= factor
        self.photo.resize(self.scale_factor * self.photo.pixmap().size())
        self.update_zoom_label()

        self.zoom_in.setEnabled(self.scale_factor < 10.0)
        self.zoom_out.setEnabled(self.scale_factor > 0.03)

    def reset_zoom(self):
        """ Reset the scaling of the image """
        self.photo.adjustSize()
        self.scale_factor = 1.0
        self.update_zoom_label()

    def fit_image(self):
        """ Fit the image to the available space """
        factor = self.scroll_area.height() / self.photo.pixmap().height()
        self.scale_factor = 1.0
        self.scale_image(factor)

    def update_zoom_label(self):
        """ Update the label of the zoom value """
        self.size_label.setText(f"{100* self.scale_factor:.0f}%")
