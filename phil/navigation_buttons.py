""" Widget to encapsulate the navigation buttons """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDataWidgetMapper


class NavigationButtons(QWidget):
    """ Encapsulates the next/prev buttons for the mapper """

    def __init__(self, mapper: QDataWidgetMapper, parent=None):
        super().__init__(parent)

        self.mapper = mapper
        layout = QHBoxLayout()

        self.first = QPushButton("First")
        self.first.pressed.connect(self.mapper.toFirst)
        layout.addWidget(self.first)

        self.back = QPushButton("Back")
        self.back.pressed.connect(self.mapper.toPrevious)
        layout.addWidget(self.back)

        layout.addStretch()

        self.submit = QPushButton("Save")
        self.submit.pressed.connect(self.mapper.submit)
        layout.addWidget(self.submit)

        self.submit_next = QPushButton("Save & Next")
        self.submit_next.pressed.connect(
            lambda: self.mapper.submit() and self.mapper.toNext()
        )
        layout.addWidget(self.submit_next)

        layout.addStretch()

        self.next = QPushButton("Next")
        self.next.pressed.connect(self.mapper.toNext)
        layout.addWidget(self.next)

        self.last = QPushButton("Last")
        self.last.pressed.connect(self.mapper.toLast)
        layout.addWidget(self.last)

        self.mapper.currentIndexChanged.connect(self.row_changed)
        self.row_changed(0)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def row_changed(self, row: int):
        """ When the mapper has moved to a new row """
        row_count = self.mapper.model().rowCount()
        self.first.setEnabled(row != 0)
        self.back.setEnabled(row != 0)
        self.submit.setEnabled(row_count != 0)
        self.submit_next.setEnabled(row_count != 0)
        self.next.setEnabled(row + 1 < row_count)
        self.last.setEnabled(row + 1 < row_count)
