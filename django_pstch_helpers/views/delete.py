from django.views.generic import DeleteView

from .mixins.base import BaseModelFormMixins

from .mixins.delete.messages import DeleteMessageMixin
from .mixins.delete.collector import DeletionCollectorContextMixin

class DeleteView(BaseModelFormMixins,
                 DeleteMessageMixin,
                 DeletionCollectorContextMixin,
                 DeleteView):
    pass
