from ...utils import contribute_viewset_to_views

from .. import AutoPatterns
from ...sets import CreateViewSet, UpdateViewSet, DeleteViewSet


class CreatableModelMixin(AutoPatterns):
    def get_create_url(self):
        return self.get_url(CreateViewSet.action,
                            args = [self.id,])
    def get_views(self):
        views = super(CreatableModelMixin, self).get_views()
        contribute_viewset_to_views(views, CreateViewSet)
        return views

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

class DeletableModelMixin(AutoPatterns):
    def get_delete_url(self):
        return self.get_url(DeleteViewSet.action,
                            args = [self.id,])
    def get_views(self):
        views = super(DeletableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DeleteViewSet)
        return views

