from .base import ViewSet
from ..views import ListView, FilteredListView

class ListViewSet(ViewSet):
    action = "list"
    url = "%s$" % (action)
    view = ListView

class FilteredListViewSet(ViewSet):
    action = "list-filtered"
    url = "%s$" % (action)
    view = FilteredListView
