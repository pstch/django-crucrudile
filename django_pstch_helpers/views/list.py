from django.views.generic import ListView
from django_filters.views import FilterView

from .mixins.base import BaseModelMixins
from .mixins.related import SelectRelatedMixin
from .mixins.list.sort import SortMixin

class ListView(BaseModelMixins, ListView, SortMixin, SelectRelatedMixin):
    pass

class FilteredListView(BaseModelMixins, FilterView, SortMixin, SelectRelatedMixin):
    pass
