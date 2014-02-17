from .base import ViewSet

from .detail import DetailViewSet
from .list import ListViewSet, FilteredListViewSet

from .edit.create import CreateViewSet, SpecificCreateViewSet
from .edit.update import UpdateViewSet
from .edit.delete import DeleteViewSet

__all__ = ['ViewSet',
           'DetailViewSet',
           'ListViewSet', 'FilteredListViewSet',
           'CreateViewSet', 'SpecificCreateViewSet',
           'UpdateViewSet',
           'DeleteViewSet']
