from django_crucrudile.views.mixins import ModelActionMixin

class AutoPatternsMixinTestView(ModelActionMixin):
    pass

class AuxAutoPatternsMixinTestView(ModelActionMixin):
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
