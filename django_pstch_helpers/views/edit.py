from django.views.generic import CreateView, UpdateView

from .mixins.base import BaseModelFormMixins
from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin
class CreateView(BaseModelFormMixins, CreateMessageMixin, CreateView):
    pass

class UpdateView(BaseModelFormMixins, UpdateMessageMixin, UpdateView):
    pass

class SpecificCreateView(BaseModelFormMixins, CreateMessageMixin, SpecificCreateMixin, CreateView):
    pass
