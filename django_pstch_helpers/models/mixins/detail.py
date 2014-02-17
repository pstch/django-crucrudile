from ...utils import contribute_viewset_to_views

from ...sets import DetailViewSet
from .base import AutoPatternsMixin

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
