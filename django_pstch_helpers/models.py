from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import AutoSlugField, CreationDateTimeField

from markitup.fields import MarkupField

from django_pstch_helpers.viewsets import BASE_VIEWS

class ModelInfo(models.Model):
    class Meta:
        abstract = True
    @classmethod
    def get_model_verbose_name(self):
        return self._meta.verbose_name
    @classmethod
    def get_count(self):
        return self.objects.count()
    @classmethod
    def get_label(self):
        return getattr(self,
                       'CUSTOM_LABEL',
                       self._meta.verbose_name)
    @classmethod
    def get_help_text(self):
        return getattr(self,
                       'HELP_TEXT',
                       None)

class AutoPatterns(ModelInfo):
    URL_NAME = None
    URL_VIEWS = BASE_VIEWS
    URL_PREFIX = None
    URL_NAMESPACES = []
    @classmethod
    def get_url(self, action, args = None):
        _namespaces = list(getattr(self, URL_ROOT_NAMESPACE, []))
        for NS in self.URL_NAMESPACES:
            _namespaces.append(NS)
        _namespaces = ":".join(_namespaces)
        _name = "%s:%s-%s" % (_namespaces,
                              self.URL_NAME,
                              action)
        try:
            return reverse(_name, args = args)
        except:
            return None
                                        
    def get_absolute_url(self):
        return self.get_url("detail", args = [self.id,])
    def get_edit_url(self):
        return self.get_url("update", args = [self.id,])
    def get_delete_url(self):
        return self.get_url("delete", args = [self.id,])

    @classmethod
    def get_list_url(self):
        return self.get_url("list")
    @classmethod
    def get_create_url(self):
        return self.get_url("create")

    class Meta:
        abstract = True

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
