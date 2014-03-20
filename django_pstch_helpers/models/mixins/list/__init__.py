"""
#TODO: Add module docstring
"""
from django_pstch_helpers.views import ListView

#pylint: disable=F0401
from ..base import AutoPatternsMixin

#pylint: enable=F0401

class ListableModelMixin(AutoPatternsMixin):
    """
    Use this Mixin with django-generic-patterns on a Model to
    automatically create "list" pages.
    """
    #pylint: disable=W0232, R0201, E1002
    @classmethod
    def get_list_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(ListView) #pylint: disable=E1120

    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(ListableModelMixin, cls).get_views()
        views.append(ListView)
        return views

    @classmethod
    def get_args_by_view(cls, view):
        """
        #TODO: Add method docstring
        """
        args = super(ListableModelMixin, cls).get_args_by_view(view)
        if view is ListView:
            args.update({
                'select_related' : cls.get_list_select_related_fields(),
                'paginate_by' : cls.get_paginate_by(),
                'allowed_sort_fields' : cls.get_sort_fields(),
            })
        return args

    @classmethod
    def get_sort_fields(cls):
        """
        Override this if you want to allow sorting. Should return a
        dict used as argument to django-sortable-listview (see
        relevant specification)
        """
        return []

    @classmethod
    def get_paginate_by(cls):
        """
        Override this if you want to use pagination. Should return an
        integer, that will be used as the value for the 'paginate_by'
        view keyword argument.
        """
        return None

    @classmethod
    def get_list_select_related_fields(cls):
        """
        Override this to tell Django on which fields it should use
        select_related (resulting in 'SQL JOINS'). Should return a list
        of fields (ex: ['category', 'category__phase'])
        """
        return []
