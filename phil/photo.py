""" Holds Photo information including metadata """

import hashlib
from os import path
from datetime import date


class Photo:
    """ Information about a photo in the model """

    BLOCK_SIZE = 65536

    def __init__(self, filepath: str):
        self.filepath = filepath
        (self.path, self.filename) = path.split(self.filepath)
        self.hash = self.generate_hash()

        self.has_metadata = False
        self.date_taken: date = None
        self.description = ""

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
