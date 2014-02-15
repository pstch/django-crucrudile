from django.views.generic import View, TemplateView, ListView, DetailView, FormView

from .mixins.base import BaseMixins, BaseModelMixins, BaseModelFormMixins
from .mixins.related import SelectRelatedMixin

class View(BaseMixins, View):
    pass

class TemplateView(BaseMixins, TemplateView):
    pass


class ListView(BaseModelMixins, ListView, SelectRelatedMixin):
    pass

class DetailView(BaseModelMixins, DetailView):
    pass

class FormView(BaseModelFormMixins, FormView):
    pass

class HomeView(TemplateView):
    pass
