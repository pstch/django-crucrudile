#TODO
from .base import ViewSet
from ..views import SpecificCreateView

class SpecificCreateViewSet(ViewSet):
    action = "create-specific"
    url = "%s/%s$" % (action,
                      "of-(?P<specific_key>\w+)/(?P<specific_value>\d+)")
    view = SpecificCreateView
