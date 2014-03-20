"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.utils import get_filter_class
from django_pstch_helpers.views import FilteredListView

#pylint: disable=F0401
from ..base import AutoPatternsMixin
#pylint: enable=F0401

class FilteredListableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_filtered_list_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(FilteredListView) # pylint: disable=E1120

    @classmethod
    def get_filter(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        raise ImproperlyConfigured(
            "get_filter should be overriden to"
            " return a proper django-filter Filter")


    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(FilteredListableModelMixin, cls).get_views()
        views.append(FilteredListView)
        return views

    @classmethod
    def get_args_by_view(cls, view):
        """
        #TODO: Add method docstring
        """
        args = super(FilteredListableModelMixin, cls).get_args_by_view(view)
        if view is FilteredListView:
            args.update({
                'select_related' : cls.get_filtered_list_select_related_fields(),
                'paginate_by' : cls.get_filtered_list_paginate_by(),
                'allowed_sort_fields' : cls.get_filtered_list_sort_fields(),
            })
        return args

    @classmethod
    def get_filtered_list_sort_fields(cls):
        """
        Override this if you want to allow sorting. Should return a
        dict used as argument to django-sortable-listview (see
        relevant specification)
        """
        return getattr(cls, 'get_sort_fields', {})

    @classmethod
    def get_filtered_list_paginate_by(cls):
        """
        Override this if you want to use pagination. Should return an
        integer, that will be used as the value for the 'paginate_by'
        view keyword argument.
        """
        return getattr(cls, 'get_paginate_by', None)

    @classmethod
    def get_filtered_list_select_related_fields(cls):
        """
        Override this to tell Django on which fields it should use
        select_related (resulting and SQL JOINS). Should return a list
        of fields (ex: ['category', 'category__phase'])
        """
        return getattr(cls, 'get_list_select_related_fields', [])
