from .base import ViewSet

from .detail import DetailViewSet
from .list import ListViewSet, FilteredListViewSet

from .edit import CreateViewSet, SpecificCreateViewSet, UpdateViewSet
from .delete import DeleteViewSet

__all__ = ['ViewSet',
           'DetailViewSet',
           'ListViewSet', 'FilteredListViewSet',
           'CreateViewSet', 'SpecificCreateViewSet',
           'UpdateViewSet',
           'DeleteViewSet']
