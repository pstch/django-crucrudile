"""
#TODO: Add module docstring for views.edit
"""
#pylint: disable=R0901, R0904
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import UpdateView as DjangoUpdateView
from django.views.generic import DeleteView as DjangoDeleteView

from .mixins.base import BaseModelFormViewMixins

from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin

from .mixins.delete.collector import DeletionCollectorContextMixin
from .mixins.delete.messages import DeleteMessageMixin

class CreateView(BaseModelFormViewMixins,
                 CreateMessageMixin,
                 DjangoCreateView):
    """
    #TODO: Add class docstring
    """
    pass

class UpdateView(BaseModelFormViewMixins,
                 UpdateMessageMixin,
                 DjangoUpdateView):
    """
    #TODO: Add class docstring
    """
    pass

class SpecificCreateView(BaseModelFormViewMixins,
                         CreateMessageMixin,
                         SpecificCreateMixin,
                         DjangoCreateView):
    """
    #TODO: Add class docstring
    """
    pass

class DeleteView(BaseModelFormViewMixins,
                 DeleteMessageMixin,
                 DeletionCollectorContextMixin,
                 DjangoDeleteView):
    """
    #TODO: Add class docstring
    """
    pass
