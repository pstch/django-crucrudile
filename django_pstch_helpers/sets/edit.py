"""
#TODO: Add module docstring
"""
from .base import ViewSet, _PK_ARG
from ..views import CreateView, SpecificCreateView, UpdateView

class CreateViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232,R0903
    action = "create"
    url = "%s$" % (action)
    view = CreateView

_SPECIFIC_ARG = r"of-(?P<specific_key>\w+)/(?P<specific_value>\d+)"

class SpecificCreateViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232,R0903
    action = "create-specific"
    url = "%s/%s$" % (action,
                      _SPECIFIC_ARG)
    view = SpecificCreateView

class UpdateViewSet(ViewSet):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232,R0903
    action = "update"
    url = "%s/%s$" % (action, _PK_ARG)
    view = UpdateView
