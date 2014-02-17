from django.views.generic import DetailView

from .mixins.base import BaseModelMixins

class DetailView(BaseModelMixins, DetailView):
    pass

