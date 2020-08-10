""" Tests for the Photo class """

from unittest import mock
from phil.photo import Photo


def test_filepath_is_split(monkeypatch):
    """ When loading a filepath, it should be split into path+filename """
    # Given
    monkeypatch.setattr(Photo, "generate_hash", lambda _: "")
    photo = Photo("C:\\Windows\\System\\test.jpg")
    photo.generate_hash = mock.MagicMock()

    # Then
    assert photo.filename == "test.jpg"
    assert photo.path == "C:\\Windows\\System"
