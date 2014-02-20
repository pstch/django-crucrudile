from .base import ViewSet, _PK_ARG
from ..views import CreateView, SpecificCreateView, UpdateView

class CreateViewSet(ViewSet):
    action = "create"
    url = "%s$" % (action)
    view = CreateView

_SPECIFIC_ARG = r"of-(?P<specific_key>\w+)/(?P<specific_value>\d+)"

class SpecificCreateViewSet(ViewSet):
    action = "create-specific"
    url = "%s/%s$" % (action,
                      _SPECIFIC_ARG)
    view = SpecificCreateView

class UpdateViewSet(ViewSet):
    action = "update"
    url = "%s/%s$" % (action, _PK_ARG)
    view = UpdateView
