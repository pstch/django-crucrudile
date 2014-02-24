"""
#TODO: Add module docstring
"""
from .base import ViewSet
from ..views import ListView, FilteredListView

class ListViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=R0903, W0232
    action = "list"
    url = "%s$" % (action)
    view = ListView

class FilteredListViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=R0903, W0232
    action = "list-filtered"
    url = "%s$" % (action)
    view = FilteredListView
