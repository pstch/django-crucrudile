from django.views.generic import UpdateView

from .mixins.base import BaseModelFormMixins

from .mixins.edit.messages import UpdateMessageMixin

class UpdateView(BaseModelFormMixins, UpdateMessageMixin, UpdateView):
    pass

