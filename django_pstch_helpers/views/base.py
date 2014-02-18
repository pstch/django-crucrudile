from django.views.generic import View, TemplateView, ListView, DetailView, FormView

from .mixins.base import BaseMixins
from .mixins.related import SelectRelatedMixin

from .mixins.auth import AuthMixin
from .mixins.context import ExtraContextMixin, ModelInfoMixin
from .mixins.redirect import ModelFormRedirectMixin
from .mixins.template import TemplateMixin


class View(BaseMixins, View):
    pass

class TemplateView(BaseMixins, TemplateView):
    pass

class HomeView(TemplateView):
    pass
