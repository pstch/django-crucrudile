from django.db.models import Model

from django_crucrudile.models.mixins import make_model_mixin

from .views import TestModelTestView

TestViewMixin = make_model_mixin(
    TestModelTestView,
    extra_funcs = {
        'get_url_prefix' : classmethod(lambda cls: 'testprefix'),
    }
)

class TestModel(TestViewMixin,
                Model):
    pass
