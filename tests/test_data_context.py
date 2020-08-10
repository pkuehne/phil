""" Test for the Data Context class """

from phil.data_context import DataContext


def test_data_model_is_not_none_by_default():
    """ Check that the photo_model is set by default """
    # Given
    context = DataContext()

    # Then
    assert context.photo_model is not None
