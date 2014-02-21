from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.sets.list import FilteredListViewSet

from . import ListableModelMixin

class FilteredListableModelMixin(ListableModelMixin):
    @classmethod
    def get_filtered_list_url(self):
        return self.get_url(FilteredListViewSet.action)
    def get_views(self):
        views = super(FilteredListableModelMixin, self).get_views()
        contribute_viewset_to_views(views, FilteredListViewSet)
        return views
    def get_views_args(self):
        action = FilteredListViewSet.action
        args = super(FilteredListableModelMixin, self).get_views_args()
        args[action] = args.get(action) or {}
        args[action] = {
            'filterset_class' : lambda a,v,m : get_filter_class(m, self.get_filter())
        }
        return args
    def get_filter(self):
        raise ImproperlyConfigured(
            "get_filter should be overriden to"
            " return a proper django-filter Filter")


