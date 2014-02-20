from .base import ViewSet, _PK_ARG
from ..views import DeleteView

class DeleteViewSet(ViewSet):
    action = "delete"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DeleteView

