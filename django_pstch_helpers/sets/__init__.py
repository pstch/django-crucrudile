from .base import ViewSet
from .views import DetailView, ListView, CreateView, UpdateView

class DetailViewSet(ViewSet):
    action = "detail"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DetailView

class ListViewSet(ViewSet):
    action = "list"
    url = "%s$" % (action)
    view = ListView

class CreateViewSet(ViewSet):
    action = "create"
    url = "%s$" % (action)
    view = CreateView

class UpdateViewSet(ViewSet):
    action = "update"
    url = "%s/%s$" % (action, _PK_ARG)
    view = UpdateView

class DeleteViewSet(ViewSet):
    action = "delete"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DeleteView


