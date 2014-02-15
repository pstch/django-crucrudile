from django.views.generic import CreateView, UpdateView

from .mixins.base import BaseModelFormMixins
from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin

class CreateView(BaseModelFormMixins, CreateMessageMixin, CreateView):
    pass

class UpdateView(BaseModelFormMixins, UpdateMessageMixin, UpdateView):
    pass
