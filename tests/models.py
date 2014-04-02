from django.db import models

from django_crucrudile.models.mixins import AutoPatternsMixin

from .views import AuxAutoPatternsMixinTestView

class AutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
    pass

class AuxAutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
    @classmethod
    def get_views(cls):
        views = super(AuxAutoPatternsMixinTestModel, cls).get_views()
        views.append(AuxAutoPatternsMixinTestView)
        return views
