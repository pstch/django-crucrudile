from django.views.generic import View, TemplateView

from .mixins.base import BaseMixins

class View(BaseMixins, View):
    pass

class TemplateView(BaseMixins, TemplateView):
    pass

class HomeView(TemplateView):
    pass
