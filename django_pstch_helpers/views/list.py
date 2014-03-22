"""
#TODO: Add module docstring
"""
# pylint: disable=R0901,R0904
from django.views.generic import ListView as DjangoListView

from django_filters.views import FilterView
from django_sortable_list import SortableListMixin # pylint: disable=F0401

from .mixins.base import BaseModelMixins
from .mixins.related import SelectRelatedMixin

class ListView(BaseModelViewMixins,
               SortableListMixin,
               SelectRelatedMixin,
               DjangoListView):
    """
    #TODO: Add class docstring
    """
    @staticmethod
    def get_action_name():
        return 'list'
    @staticmethod
    def get_url_part():
        return self.get_action_name()

class FilteredListView(BaseModelViewMixins,
                       SortableListMixin,
                       SelectRelatedMixin,
                       FilterView):
    """
    #TODO: Add class docstring
    #TODO: Could we make it a mixin ?
    """
    @staticmethod
    def get_action_name():
        return 'filtered-list'
    def get_url_part():
        return self.get_action_name()

