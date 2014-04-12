from django.db.models import Model

from django_crucrudile.models.mixins import make_model_mixin

from .views import TestModelTestView

class TestModel(make_model_mixin(TestModelTestView),
                Model):
    pass
