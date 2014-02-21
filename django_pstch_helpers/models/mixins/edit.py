#TODO: Fix module docstring
from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.utils import contribute_viewset_to_views

from .base import AutoPatternsMixin

from django_pstch_helpers.sets import CreateViewSet, UpdateViewSet
from django_pstch_helpers.sets.edit import SpecificCreateViewSet

class CreatableModelMixin(AutoPatternsMixin):
    def get_create_url(self):
        return self.get_url(CreateViewSet.action,
                            args=[self.id,])
    def get_views(self):
        views = super(CreatableModelMixin, self).get_views()
        contribute_viewset_to_views(views, CreateViewSet)
        return views

class SpecificCreatableModelMixin(CreatableModelMixin):
    def get_views(self):
        views = super(SpecificCreatableModelMixin, self).get_views()
        contribute_viewset_to_views(views, SpecificCreateViewSet)
        return views
    def get_views_args(self):
        action = SpecificCreateViewSet.action
        args = super(SpecificCreatableModelMixin, self).get_views_args()
        args[action] = args.get() or {}
        args[action] = {
            'initial_keys' : self.get_specific_create_initial_keys()
        }
        return args
    @staticmethod
    def get_spec_create_init_keys():
        raise ImproperlyConfigured(
            "get_specific_create_initial_keys should be "
            "overriden to return a proper list of fields"
        )

class UpdatableModelMixin(AutoPatternsMixin):
    def get_update_url(self):
        return self.get_url(UpdateViewSet.action,
                            args=[self.id,])
    def get_edit_url(self):
        return self.get_update_url()
    def get_views(self):
        views = super(UpdatableModelMixin, self).get_views()
        contribute_viewset_to_views(views, UpdateViewSet)
        return views
