""" Provides a proxy model to pick only those photos that match a selection """

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from phil.photo_model import PhotoModel

# from phil.models.task_matcher import TaskMatcher


class FilterModel(QSortFilterProxyModel):
    """ Filters the input TreeModel to a table model of only the tasks """

    def __init__(self):
        super(FilterModel, self).__init__()
        self.person_filter = ""

    def set_person_filter(self, person: str):
        """ Sets the person to filter on """
        self.person_filter = person
        self.invalidate()

    def index_has_person(self, index: QModelIndex):
        """ Test whether the given index has a person link that we're filtering for """
        if self.person_filter == "":
            return True

        persons = index.siblingAtColumn(PhotoModel.Columns.PERSONS).data(Qt.EditRole)

        for person in persons:
            if person.name == self.person_filter:
                return True
        return False

    def filterAcceptsRow(
        self, row, parent=QModelIndex()
    ):  # pylint: disable=invalid-name
        """ Whether this row is part of the filtered view """

        index = self.sourceModel().index(row, 0, parent)
        if not index.isValid():
            return False

        return self.index_has_person(index)
        # return self.task_matcher.match(node.data, node.parent.data)
