"""
#TODO: Add module docstring
"""
from django_pstch_helpers.utils import contribute_viewset_to_views

from django_pstch_helpers.sets import DetailViewSet, ListViewSet

#pylint: disable=F0401
from ..base import AutoPatternsMixin
#pylint: enable=F0401

class ListableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232, R0201, E1002
    @classmethod
    def get_list_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(ListViewSet.action) #pylint: disable=E1120

    def get_views(self):
        """
        #TODO: Add method docstring
        """
        views = super(ListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, ListViewSet)
        return views
    def get_views_args(self):
        """
        #TODO: Add method docstring
        """
        args = super(ListableModelMixin, self).get_views_args()
        args[ListViewSet.action] = args.get(ListViewSet.action) or {}
        args[ListViewSet.action].update({
            'select_related' : self.get_list_select_related_fields(),
            'paginate_by' : self.get_paginate_by(),
            'allowed_sort_fields' : self.get_sort_fields(),
        })
        return args
    def get_sort_fields(self):
        """
        Override this if you want to allow sorting. Should return a
        dict used as argument to django-sortable-listview (see
        relevant specification)
        """
        return []
    def get_paginate_by(self):
        """
        Override this if you want to use pagination. Should return an
        integer, that will be used as the value for the 'paginate_by'
        view keyword argument.
        """
        return None
    def get_list_select_related_fields(self):
        """
        Override this to tell Django on which fields it should use
        select_related (resulting and SQL JOINS). Should return a list
        of fields (ex: ['category', 'category__phase'])
        """
        return []
