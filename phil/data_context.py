""" Holds all data models for the application """

from dataclasses import dataclass
from phil.photo_model import PhotoModel


@dataclass
class DataContext:
    """ Holder of all data models """

    photo_model: PhotoModel

    def __init__(self, photo_model=None):
        self.photo_model = photo_model if photo_model else PhotoModel()
