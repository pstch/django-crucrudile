from django.db.models import Model

from django_crucrudile.models.mixins import make_model_mixin

from .views import TestModelTestView

TestViewMixin = make_model_mixin(
    TestModelTestView,
    guess_url_namespace=True
)

class TestModel(TestViewMixin,
                Model):
    pass
