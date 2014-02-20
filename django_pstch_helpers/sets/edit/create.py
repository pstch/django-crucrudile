from .base import ViewSet
from ..views import CreateView
from ..views import SpecificCreateView

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
