from ..utils import contribute_viewset_to_views

from . import AutoPatternsMixin
from ..sets import DeleteViewSet

class DeletableModelMixin(AutoPatternsMixin):
    def get_delete_url(self):
        return self.get_url(DeleteViewSet.action,
                            args = [self.id,])
    def get_views(self):
        views = super(DeletableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DeleteViewSet)
        return views

