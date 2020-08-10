""" Image + controls for the display of a photo """

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImageReader
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton


class PhotoViewer(QWidget):
    """ Displays details of a photo """

    def __init__(self, parent=None):
        super().__init__(parent)

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
        zoom_zero = QPushButton("Original")
        zoom_zero.pressed.connect(self.reset_zoom)
        image_controls.addWidget(zoom_zero)
        zoom_fit = QPushButton("Fit")
        zoom_fit.pressed.connect(self.fit_image)
        image_controls.addWidget(zoom_fit)
        self.zoom_in = QPushButton("+")
        self.zoom_in.pressed.connect(lambda: self.scale_image(1.25))
        image_controls.addWidget(self.zoom_in)
        self.reset_zoom()
        layout.addLayout(image_controls)

        self.setLayout(layout)

    def load_image(self, filepath: str):
        """ The selected photo has changed """
        reader = QImageReader(filepath)
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
