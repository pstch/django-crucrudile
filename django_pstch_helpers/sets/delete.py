"""
#TODO: Add module docstring
"""
from .base import ViewSet, _PK_ARG
from ..views import DeleteView

class DeleteViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=R0903, W0232
    action = "delete"
    url = "%s/%s$" % (action, _PK_ARG)
    view = DeleteView

