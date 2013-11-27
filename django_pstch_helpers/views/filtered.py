from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from django_filters.views import BaseFilterView

from .mixins import AuthMixin, ModelInfoMixin

class FilteredListView(AuthMixin, ModelInfoMixin, BaseFilterView):
    template_name_suffix = '_list_filtered'
