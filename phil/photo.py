""" Holds Photo information including metadata """

import hashlib
from os import path


class Photo:
    """ Information about a photo in the model """

    BLOCK_SIZE = 65536

    def __init__(self, filepath: str):
        self.init_photo_data(filepath)
        self.init_meta_data()

        self.setup_filename()
        self.hash = self.generate_hash()

    def init_photo_data(self, filepath: str):
        """ Loads information about the photo """
        self.filepath = filepath
        self.hash = ""
        self.filename = ""
        self.path = ""

    def init_meta_data(self):
        """ Loads the metadata for the photo """
        self.has_metadata = False
        self.date_taken = None
        self.description = ""

    def setup_filename(self):
        """ Splits the filepath into path and filename """
        (self.path, self.filename) = path.split(self.filepath)

    def generate_hash(self):
        """ Generates a hash of the file contents """

        if self.filepath == "":
            return ""

        file_hash = hashlib.sha256()
        with open(self.filepath, "rb") as photo:
            block = photo.read(self.BLOCK_SIZE)
            while len(block) > 0:
                file_hash.update(block)
                block = photo.read(self.BLOCK_SIZE)
        return file_hash.hexdigest()
