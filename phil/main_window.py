""" Main Window """

from PyQt5.QtCore import QDirIterator, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from phil.list_screen import ListScreen
from phil.menu_bar import MenuBar
from phil.photo_model import Photo
from phil.data_context import DataContext


class MainWindow(QMainWindow):
    """ The Main Window where we start """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_context = DataContext()
        self.list_screen = ListScreen(self.data_context, self)

        self.setup_window()
        self.link_actions()

    def setup_window(self):
        """ Basic window setup """
        self.setWindowIcon(QIcon(":/icons/phil.ico"))
        self.setWindowTitle("Phil - The Photo/Individual Linker")

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.list_screen)

    def link_actions(self):
        """ Link menu_bar actions to things to do """
        self.menu_bar.file_open_folder_action.triggered.connect(self.load_folder)

    def load_folder(self):
        """ Load all the files in a fodler """
        folder_name = QFileDialog.getExistingDirectory(self, "Open a folder", ".")
        if folder_name == "":
            return

        print(f"Opening folder: {folder_name}")

        extensions = ["*.jpg", "*.jpeg", "*.bmp"]
        iterator = QDirIterator(
            folder_name, extensions, QDir.Files, QDirIterator.Subdirectories
        )
        photos = []
        while iterator.hasNext():
            photos.append(Photo(iterator.next()))
        self.data_context.photo_model.update_photo_list(photos)
