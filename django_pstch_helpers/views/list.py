from django.views.generic import ListView

from django_filters.views import FilterView
from django_sortable_list import SortableListMixin

from .mixins.base import BaseModelMixins
from .mixins.related import SelectRelatedMixin

class ListView(BaseModelMixins, SortableListMixin, SelectRelatedMixin, ListView):
    pass

class FilteredListView(BaseModelMixins, SortableListMixin, SelectRelatedMixin, FilterView):
    pass
