from .base import View, TemplateView, HomeView

from .list import ListView, FilteredListView
from .detail import DetailView

from .edit.create import CreateView, SpecificCreateView
from .edit.update import UpdateView
from .edit.delete import DeleteView

from .delete import *

__all__ = [
    'View', 'TemplateView', 'HomeView',
    'ListView', 'FilteredListView',
    'DetailView',
    'CreateView', 'SpecificCreateView',
    'UpdateView',
    'DeleteView',
    'SpecificCreateView'
]
