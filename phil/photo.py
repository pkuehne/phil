""" Holds Photo information including metadata """

from typing import List
import hashlib
from os import path
from datetime import date
import yaml


class Person:
    """ Person linked to a photo """

    def __init__(self, data=None):
        self.name = ""
        self.link_id = ""
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0

        if data is not None:
            self.from_dict(data)

    def from_dict(self, data):
        """ Loads fields from dict """
        self.name = data.get("name", "")
        self.link_id = data.get("link_id", "")
        self.top = data.get("top", 0)
        self.left = data.get("left", 0)
        self.bottom = data.get("bottom", 0)
        self.right = data.get("right", 0)

    def to_dict(self):
        """ Converts to pythonic representation """
        data = {}
        data["name"] = self.name
        data["link_id"] = self.link_id
        data["top"] = self.top
        data["left"] = self.left
        data["bottom"] = self.bottom
        data["right"] = self.right
        return data


class Photo:
    """ Information about a photo in the model """

    BLOCK_SIZE = 65536

    def __init__(self, filepath: str):
        self.filepath = filepath
        (self.path, self.filename) = path.split(self.filepath)
        self.hash = self.generate_hash()

        self.has_metadata = False
        self.persons: List[Person] = []
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
            data["persons"] = []
            for person in self.persons:
                data["persons"].append(person.to_dict())
            yaml.dump(data, file)

    def read_metadata(self):
        """ Reads the metadata from the yaml file """
        if not path.isfile(self.metadata_filepath()):
            return
        with open(self.metadata_filepath()) as file:
            data = yaml.safe_load(file)
            self.has_metadata = True
            self.description = data.get("description", "")
            self.date_taken = data.get("date_taken", None)
            for person_data in data.get("persons", []):
                self.persons.append(Person(person_data))
