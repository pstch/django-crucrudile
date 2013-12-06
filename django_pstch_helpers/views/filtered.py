from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from django_filters.views import FilterView

from .mixins import AuthMixin, ModelInfoMixin, SelectRelatedMixin

from sortable_listview import SortableListView

def get_filter_class(filter_model, filter_class):
    class FilterSet(filter_class):
        lookup_type = None
        class Meta(filter_class.Meta):
            model = filter_model
    return FilterSet

    
class FilteredListView(AuthMixin, ModelInfoMixin, FilterView, SortableListView, SelectRelatedMixin):
    template_name_suffix = '_list_filtered'
   def get_queryset(self):
       qs = super(FilteredListView, self).get_queryset()
       raise Exception
       qs = qs.order_by(self.sort)
       
       return qs
    def get_template_names(self):
        names = super(FilteredListView, self).get_template_names()
        names.append("%s/%s_list.html" % (self.model._meta.app_label,
                                          self.model._meta.model_name))
        names.append("%s/object_list_filtered.html" % self.model._meta.app_label)
        return names
        
