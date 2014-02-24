"""
#TODO: Add module docstring
"""
from .base import ViewSet, _PK_ARG
from ..views import DetailView

class DetailViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232,R0903
    action = "detail"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DetailView
