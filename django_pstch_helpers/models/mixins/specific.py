from django.core.exceptions import ImproperlyConfigured

from .edit import CreatableModelMixin
from ...sets.specific import SpecificCreateViewSet

class SpecificCreatableModelMixin(CreatableModelMixin):
    def get_views(self):
        views = super(ListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, SpecificCreateViewSet)
        return views
    def get_views_args(self):
        args = super(FilteredListableModelMixin, self).get_views_args()
        args[SpecificCreateViewSet.action] = args.get(SpecificCreateViewSet.action) or {}
        args[SpecificCreateViewSet.action] = {
            'initial_keys' : self.get_specific_create_initial_keys()
        }
        return args
    def get_specific_create_initial_keys(self):
        raise ImproperlyConfigured("get_specific_create_initial_keys should be overriden to return a proper list of fields")


