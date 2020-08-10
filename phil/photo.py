""" Holds Photo information including metadata """

import hashlib
from os import path
from datetime import date
import yaml


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

        self.read_metadata()

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

    def metadata_filepath(self):
        """ Returns the path and name of the metadata file """
        return path.join(self.path, path.splitext(self.filename)[0] + ".yml")

    def write_metadata(self):
        """ Writes the metadata to a yaml file """
        with open(self.metadata_filepath(), "w") as file:
            data = {}
            data["description"] = self.description
            data["date_taken"] = self.date_taken
            yaml.dump(data, file)
            print(f"Wrote {self.metadata_filepath()} with {data}")

    def read_metadata(self):
        """ Reads the metadata from the yaml file """
        if not path.isfile(self.metadata_filepath()):
            return
        with open(self.metadata_filepath()) as file:
            data = yaml.safe_load(file)
            print(f"Data: {data}")
            self.has_metadata = True
            self.description = data.get("description", "")
            self.date_taken = data.get("date_taken", None)
