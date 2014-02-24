"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import DeleteView as DjangoDeleteView

from .mixins.base import BaseModelFormMixins

from .mixins.delete.messages import DeleteMessageMixin
from .mixins.delete.collector import DeletionCollectorContextMixin

class DeleteView(BaseModelFormMixins,
                 DeleteMessageMixin,
                 DeletionCollectorContextMixin,
                 DjangoDeleteView):
    """
    #TODO: Add class docstring
    """
    pass
