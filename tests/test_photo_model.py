""" Tests for the photo model """

from PyQt5.QtCore import QModelIndex
from phil.photo_model import PhotoModel
from phil.photo import Photo


def test_column_count_matches():
    """ Check that the column count is non-zero """
    # Given
    model = PhotoModel()

    # Then
    assert model.columnCount() != 0


def test_column_count_is_zero_for_valid_parent():
    """ Photos themselves have no sub-items so, should show no columns for those """
    # Given
    model = PhotoModel([Photo("")])

    # Then
    assert model.columnCount(model.index(0, 0)) == 0


def test_row_count():
    """ Check that the row count works correctly """
    # Given
    empty_model = PhotoModel()
    valid_model = PhotoModel([Photo("")])

    # Then
    assert empty_model.rowCount() == 0
    assert valid_model.rowCount() == 1
    assert valid_model.rowCount(valid_model.index(0, 0)) == 0


def test_data_returns_none_for_invalid_index():
    """ When the passed index is invalid, no data should be returned """
    # Given
    photo = Photo("")
    model = PhotoModel([photo])

    # When
    data = model.data(QModelIndex())

    # Then
    assert data is None


def test_data_returns_data_in_photo():
    """ When the passed index is invalid, no data should be returned """
    # Given
    photo = Photo("")
    photo.hash = "FOO"
    model = PhotoModel([photo])

    # When
    data = model.data(model.index(0, model.Columns.HASH))

    # Then
    assert data is photo.hash


def test_update_photo_list_emits_signals(qtbot):
    """ When the photo list is updated the reset model signals should be emitted """
    # Given
    model = PhotoModel()

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.update_photo_list([Photo("")])

    # Then
    assert model.rowCount() == 1
