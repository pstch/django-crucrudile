from .base import ViewSet

from ..views import FilteredListView

class FilteredListViewSet(ViewSet):
    action = "list-filtered"
    url = "%s$" % (action)
    view = FilteredListView
