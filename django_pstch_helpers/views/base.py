from django.views.generic import View, TemplateView, ListView, DetailView, FormView

from .mixins.base import BaseModelMixins
from .mixins.related import SelectRelatedMixin


class View(BaseMixins, View):
    pass

class TemplateView(BaseMixins, TemplateView):
    pass

class HomeView(TemplateView):
    pass
