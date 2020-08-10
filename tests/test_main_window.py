""" Tests for the main window """

from PyQt5.QtWidgets import QFileDialog
from phil.main_window import MainWindow


def test_load_folder_does_nothin_if_aborted(qtbot, monkeypatch):
    """ If the user aborts opening a folder, nothing should happen """

    # Given
    window = MainWindow()
    qtbot.addWidget(window)
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda _, __, ___: "")

    # When
    window.load_folder()

    # Then
