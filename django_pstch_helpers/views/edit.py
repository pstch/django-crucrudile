#TODO: Add module docstring
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import UpdateView as DjangoUpdateView

from .mixins.base import BaseModelFormMixins
from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin

class CreateView(BaseModelFormMixins,
                 CreateMessageMixin,
                 CreateView):
    pass

class UpdateView(BaseModelFormMixins,
                 UpdateMessageMixin,
                 DjangoUpdateView):
    pass

class SpecificCreateView(BaseModelFormMixins,
                         CreateMessageMixin,
                         SpecificCreateMixin,
                         DjangoCreateView):
    pass
