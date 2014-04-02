from django.db import models

from django_crucrudile.models.mixins import AutoPatternsMixin

class AutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
    pass
