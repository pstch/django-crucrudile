from django.db import models

from django_extensions.db.models import AutoSlugField # Used in UserNamed
from markitup.fields import MarkupField # Used in UserDescribed

from .mixins import ModelInfoMixin

class UserNamed(ModelInfoMixin, models.Model):
    #TODO: Write tests for this class (test at least that __unicode__ is working well) using a sample model
    name = models.CharField(max_length=128, verbose_name="name")
    slug = AutoSlugField(populate_from='name')
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True

class UserDescribed(UserNamed):
    #TODO: Write tests for this class (test at least that the description can be rendered to HTML) using a sample model
    description = MarkupField(blank=True, null=True, verbose_name="description")
    class Meta:
        abstract = True
