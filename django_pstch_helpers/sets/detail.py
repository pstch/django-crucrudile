from .base import ViewSet
from ..views import DetailView


class DetailViewSet(ViewSet):
    action = "detail"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DetailView
