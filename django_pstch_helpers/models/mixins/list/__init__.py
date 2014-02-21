from django_pstch_helpers.utils import contribute_viewset_to_views

from django_pstch_helpers.sets import DetailViewSet, ListViewSet

from ..base import AutoPatternsMixin

class ListableModelMixin(AutoPatternsMixin):
    @classmethod
    def get_list_url(self):
        return self.get_url(ListViewSet.action)
    def get_views(self):
        views = super(ListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, ListViewSet)
        return views
    def get_views_args(self):
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
        Override this if you want to allow sorting. Should return a dict used as argument to django-sortable-listview (see relevant specification)
        """
        return []
    def get_paginate_by(self):
        """
        Override this if you want to use pagination. Should return an integer, that will be used as the value for the 'paginate_by' view keyword argument.
        """
        return None
    def get_list_select_related_fields(self):
        """
        Override this to tell Django on which fields it should use select_related (resulting and SQL JOINS). Should return a list of fields (ex: ['category', 'category__phase'])
        """
        return []
