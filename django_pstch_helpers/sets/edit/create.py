from .base import ViewSet
from ..views import CreateView
from ..views import SpecificCreateView

class CreateViewSet(ViewSet):
    action = "create"
    url = "%s$" % (action)
    view = CreateView

class SpecificCreateViewSet(ViewSet):
    action = "create-specific"
    url = "%s/%s$" % (action,
                      "of-(?P<specific_key>\w+)/(?P<specific_value>\d+)")
    view = SpecificCreateView
