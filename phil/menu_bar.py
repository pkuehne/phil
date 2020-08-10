""" MenuBar for the MainWindow """

import sys
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from version import MAJOR, MINOR, PATCH


class MenuBar(QMenuBar):
    """ MenuBar """

    about_string = "Copyright (c) 2020 by Peter Kühne\nIcons from https://icons8.com"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_file_menu()
        self.setup_help_menu()

    def setup_file_menu(self):
        """ Create the File menu """
        self.file_open_folder_action = QAction("&Open Folder", self)
        self.file_open_folder_action.setShortcut("CTRL+O")

        self.file_quit_action = QAction("&Quit", self)
        self.file_quit_action.setShortcut("CTRL+Q")
        self.file_quit_action.triggered.connect(sys.exit)

        file_menu = self.addMenu("&File")
        file_menu.addAction(self.file_open_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(self.file_quit_action)

    def setup_help_menu(self):
        """ Create the Help menu """
        self.help_about_action = QAction("&About", self)
        about_text = f"Version: {MAJOR}.{MINOR}.{PATCH}\n\n{MenuBar.about_string}"
        self.help_about_action.triggered.connect(
            lambda: QMessageBox.about(self, "About", about_text)
        )
        help_menu = self.addMenu("&Help")
        help_menu.addAction(self.help_about_action)
