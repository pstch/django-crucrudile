"""
#TODO: Add module docstring for views.edit
"""
#pylint: disable=R0901, R0904
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import UpdateView as DjangoUpdateView
from django.views.generic import DeleteView as DjangoDeleteView

from .mixins.base import BaseModelFormMixins

from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin

from .mixins.delete.collector import DeletionCollectorContextMixin
from .mixins.delete.messages import DeleteMessageMixin

class CreateView(BaseModelFormMixins,
                 CreateMessageMixin,
                 DjangoCreateView):
    """
    #TODO: Add class docstring
    """
    pass

class UpdateView(BaseModelFormMixins,
                 UpdateMessageMixin,
                 DjangoUpdateView):
    """
    #TODO: Add class docstring
    """
    pass

class SpecificCreateView(BaseModelFormMixins,
                         CreateMessageMixin,
                         SpecificCreateMixin,
                         DjangoCreateView):
    """
    #TODO: Add class docstring
    """
    pass

class DeleteView(BaseModelFormMixins,
                 DeleteMessageMixin,
                 DeletionCollectorContextMixin,
                 DjangoDeleteView):
    """
    #TODO: Add class docstring
    """
    pass
