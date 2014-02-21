from django_pstch_helpers.utils import contribute_viewset_to_views

from django_pstch_helpers.sets import DeleteViewSet

from .base import AutoPatternsMixin

class DeletableModelMixin(AutoPatternsMixin):
    def get_delete_url(self):
        return self.get_url(DeleteViewSet.action,
                            args=[self.id,])
    def get_views(self):
        views = super(DeletableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DeleteViewSet)
        return views

