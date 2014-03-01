"""
#TODO: Add module docstring
"""
#pylint: disable=F0401
from ..base import AutoPatternsMixin
#pylint: enable=F0401

class ListableModelMixin(object):
    """
    #TODO: Add class docstring
    """
    #pylint: disable=W0232, R0201, E1002
    @classmethod
    def get_list_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url('list') #pylint: disable=E1120

    def get_views(self):
        """
        #TODO: Add method docstring
        """
        views = super(ListableModelMixin, self).get_views()
        views.append(ListView)
        return views
    def get_args_by_view(self, view):
        """
        #TODO: Add method docstring
        """
        args = super(ListableModelMixin, self).get_args_by_view(view)
        if view is ListView:
            args.append({
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
