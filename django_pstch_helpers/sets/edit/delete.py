from .base import ViewSet
from ..views import DeleteView

class DeleteViewSet(ViewSet):
    action = "delete"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DeleteView

