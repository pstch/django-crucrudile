from django.views.generic import CreateView

from .mixins.base import BaseModelFormMixins

from .mixins.edit.messages import CreateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin

class CreateView(BaseModelFormMixins, CreateMessageMixin, CreateView):
    pass

class SpecificCreateView(BaseModelFormMixins, CreateMessageMixin, SpecificCreateMixin, CreateView):
    pass
