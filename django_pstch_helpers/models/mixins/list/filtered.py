"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.utils import (contribute_viewset_to_views,
                                        get_filter_class)
from django_pstch_helpers.sets.list import FilteredListViewSet

from . import ListableModelMixin

class FilteredListableModelMixin(ListableModelMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_filtered_list_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(FilteredListViewSet.action) # pylint: disable=E1120
    def get_views(self):
        """
        #TODO: Add method docstring
        """
        views = super(FilteredListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, FilteredListViewSet)
        return views
    def get_views_args(self):
        """
        #TODO: Add method docstring
        """
        action = FilteredListViewSet.action
        args = super(FilteredListableModelMixin, self).get_views_args()
        args[action] = args.get(action) or {}
        args[action] = {
            'filterset_class' : \
            lambda a, v, m: get_filter_class(m, self.get_filter())
        }
        return args
    def get_filter(self):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        raise ImproperlyConfigured(
            "get_filter should be overriden to"
            " return a proper django-filter Filter")


