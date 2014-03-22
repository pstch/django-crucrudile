"""
#TODO: Add module docstring
"""
# pylint: disable=R0901,R0904
from django.views.generic import ListView as DjangoListView

from django_filters.views import FilterView
from django_sortable_list import SortableListMixin # pylint: disable=F0401

from .mixins.base import BaseModelViewMixins
from .mixins.related import SelectRelatedMixin

class ListView(BaseModelViewMixins,
               SortableListMixin,
               SelectRelatedMixin,
               DjangoListView):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return 'list'
    @classmethod
    def get_url_part(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_action_name()

class FilteredListView(BaseModelViewMixins,
                       SortableListMixin,
                       SelectRelatedMixin,
                       FilterView):
    """
    #TODO: Add class docstring
    #TODO: Could we make it a mixin ?
    """
    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return 'filtered-list'
    @classmethod
    def get_url_part(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_action_name()

