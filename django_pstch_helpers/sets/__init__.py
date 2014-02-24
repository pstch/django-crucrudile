"""
#TODO: Add module docstring
"""
#pylint: disable=F0401
from .base import ViewSet

from .detail import DetailViewSet
from .list import ListViewSet, FilteredListViewSet

from .edit import CreateViewSet, SpecificCreateViewSet, UpdateViewSet
from .delete import DeleteViewSet
#pylint: enable=F0401

__all__ = ['ViewSet',
           'DetailViewSet',
           'ListViewSet', 'FilteredListViewSet',
           'CreateViewSet', 'SpecificCreateViewSet',
           'UpdateViewSet',
           'DeleteViewSet']
