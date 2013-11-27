from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from django_filters.views import FilterView

from .mixins import AuthMixin, ModelInfoMixin

class FilteredListView(AuthMixin, ModelInfoMixin, FilterView):
    template_name_suffix = '_list_filtered'
