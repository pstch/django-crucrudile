from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django_crucrudile.views.mixins import ModelActionMixin

class TestModelTestView(ModelActionMixin, SingleObjectMixin, View):
    action = 'test-action'

class AutoPatternsMixinTestView(ModelActionMixin, SingleObjectMixin, View):
    pass

class AuxAutoPatternsMixinTestView(ModelActionMixin, SingleObjectMixin, View):
    pass

class MakeModelMixinTestView(ModelActionMixin, SingleObjectMixin, View):
    pass

class ModelActionMixinTestView(ModelActionMixin, View):
    pass

class MakeModelMixinWithoutViewMixinTestView(SingleObjectMixin, View):
    pass

class MakeModelMixinsFirstTestView(ModelActionMixin, View):
    pass

class MakeModelMixinsSecondTestView(View):
    pass

class MakeModelMixinsThirdTestView(View):
    pass
