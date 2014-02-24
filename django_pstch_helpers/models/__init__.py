"""
#TODO: Add module docstring
"""
from django.db import models

from django_extensions.db.models import AutoSlugField # Used in UserNamed
from markitup.fields import MarkupField # Used in UserDescribed

#pylint: disable=F0401
from .mixins import ModelInfoMixin
#pylint: enable=F0401

class UserNamed(models.Model):
    """
    #TODO: Add class docstring
    """
    #TODO: Write tests for this class
    # (test at least that __unicode__ is working well using a sample model)
    name = models.CharField(max_length=128, verbose_name="name")
    slug = AutoSlugField(populate_from='name')
    def __unicode__(self):
        """
        #TODO: Add method docstring
        """
        return self.name
    class Meta:
        """
        #TODO: Add class docstring
        """
        #pylint: disable=W0232,C1001,R0903
        abstract = True

class UserDescribed(UserNamed):
    """
    #TODO: Add class docstring
    """
    #TODO: Write tests for this class
    # (test at least that the description
    # can be rendered to HTML using a sample model)
    description = MarkupField(blank=True, null=True, verbose_name="description")
    class Meta:
        """
        #TODO: Add class docstring
        """
        #pylint: disable=W0232,C1001,R0903
        abstract = True
