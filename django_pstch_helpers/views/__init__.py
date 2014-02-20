from .base import View, TemplateView, HomeView

from .list import ListView, FilteredListView
from .detail import DetailView

from .edit import CreateView, SpecificCreateView, UpdateView
from .delete import DeleteView

from .delete import DeleteView

__all__ = [
    'View', 'TemplateView', 'HomeView',
    'ListView', 'FilteredListView',
    'DetailView',
    'CreateView', 'SpecificCreateView',
    'UpdateView',
    'DeleteView',
    'SpecificCreateView'
]
