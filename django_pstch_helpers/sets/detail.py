from .base import ViewSet, _PK_ARG
from ..views import DetailView


class DetailViewSet(ViewSet):
    action = "detail"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DetailView
