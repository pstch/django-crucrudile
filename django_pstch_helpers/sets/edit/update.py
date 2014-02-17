from .base import ViewSet
from ..views import UpdateView

class UpdateViewSet(ViewSet):
    action = "update"
    url = "%s/%s$" % (action, _PK_ARG)
    view = UpdateView
