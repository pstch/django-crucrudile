from .base import ViewSet, _PK_ARG
from ..views import UpdateView

class UpdateViewSet(ViewSet):
    action = "update"
    url = "%s/%s$" % (action, _PK_ARG)
    view = UpdateView
