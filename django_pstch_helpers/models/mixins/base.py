from ...utils import contribute_viewset_to_views

from .. import AutoPatterns
from ...sets import DetailViewSet, ListViewSet

class DetailableModelMixin(AutoPatterns):
    def get_detail_url(self):
        return self.get_url(DetailViewSet.action,
                            args = [self.id,])
    def get_absolute_url(self):
        return self.get_detail_url()
    def get_views(self):
        views = super(DetailableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DetailViewSet)
        return views

class ListableModelMixin(AutoPatterns):
    @classmethod
    def get_list_url(self):
        return self.get_url(ListViewSet.action)
    def get_views(self):
        views = super(ListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, ListViewSet)
        return views
    def get_views_args(self):
        args = super(ListableModelMixin, self).get_views_args()
        args[ListViewSet.action] = { 'select_related' : self.get_list_select_related_fields(),}
        return args
    def get_list_select_related_fields():
        """
        Override this to tell Django on which fields it should use select_related (resulting and SQL JOINS). Should return a list of fields (ex: ['category', 'category__phase'])
        """
        return []

