from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import AutoSlugField, CreationDateTimeField

from markitup.fields import MarkupField

from .views.sets import BASE_VIEWS

class ModelInfo():
    @classmethod
    def _get_objects(self):
        try:
            objects = self.objects
            return objects
        except AttributeError:
            raise ImproperlyConfigured("Could not find manager : \"objects\" not present on the current object. Check that ModelInfoMixin is used on a Model.")

    @classmethod
    def _get_meta(self):
        try:
            _meta = self._meta
            return _meta
        except AttributeError:
            raise ImproperlyConfigured("Could not find Meta class : \"_meta\" not present on the current object. Check that ModelInfoMixin is used on a Model.")

    @classmethod
    def get_verbose_name(self):
        _meta = self._get_meta()
        return _meta.verbose_name
    @classmethod
    def get_count(self):
        objects = self._get_objects()
        return self.objects.count()
    @classmethod
    def get_model_name(self):
        _meta = self._get_meta()
        return _meta.model_name

class AutoPatterns(ModelInfo):
    def get_url_name(self):
        return self.get_model_name()
    def get_url_prefix(self):
        return None
    def get_views(self):
        return {} # hey, BASE_VIEWS
    def get_view_args(self):
        return {}
    def get_url_namespaces(self):
        return []
    @classmethod
    def _make_url_name(action):
        return make_url_name(self.get_url_namespaces(),
                             self.get_url_name(),
                             action)
    def get_url(self, action, args = None):
        return reverse(self._make_url_name(action),
                           args = args)

class UserNamed(ModelInfo):
    name = models.CharField(max_length = 128, verbose_name = "name")
    slug = AutoSlugField(populate_from = 'name')
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True

class UserDescribed(UserNamed):
    description = MarkupField(blank = True, null = True, verbose_name = "description")
    class Meta:
        abstract = True


# ANNEX (new branch code)

class DetailableModelMixin(AutoPatterns):
    def get_detail_url(self):
        return self.get_url(DetailViewSet.action,
                            args = [self.id,])
    def get_absolute_url(self):
        return self.get_detail_url()
    def get_views(self):
        views = super(DetailableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DetailViewSet)
        return views

class ListableModelMixin(AutoPatterns):
    @classmethod
    def get_list_url(self):
        return self.get_url(ListViewSet.action)
        def get_views(self):
            views = super(ListableModelMixin, self).get_views()
            contribute_viewset_to_views(views, ListViewSet)
            return views

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

