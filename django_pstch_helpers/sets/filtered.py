from .base import ViewSet

class FilteredListViewSet(ViewSet):
    action = "list-filtered"
    url = "%s$" % (action)
    view = FilteredListView
