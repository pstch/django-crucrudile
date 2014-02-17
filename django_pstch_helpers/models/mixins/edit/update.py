from ...utils import contribute_viewset_to_views

from .. import AutoPatterns
from ...sets import UpdateViewSet

class UpdatableModelMixin(AutoPatterns):
    def get_update_url(self):
        return self.get_url(UpdateViewSet.action,
                            args = [self.id,])
    def get_edit_url(self):
        return self.get_update_url()
        def get_views(self):
        views = super(UpdatableModelMixin, self).get_views()
        contribute_viewset_to_views(views, UpdateViewSet)
        return views
