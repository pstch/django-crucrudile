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

class MakeModelMixinTestView(ModelActionMixin):
    pass

class ModelActionMixinTestView(ModelActionMixin):
    pass

class MakeModelMixinWithoutViewMixinTestView(object):
    pass

class MakeModelMixinsFirstTestView(ModelActionMixin):
    pass

class MakeModelMixinsSecondTestView(object):
    pass

class MakeModelMixinsThirdTestView(object):
    pass
