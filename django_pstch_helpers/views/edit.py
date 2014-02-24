"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import CreateView as DjangoCreateView
from django.views.generic import UpdateView as DjangoUpdateView

from .mixins.base import BaseModelFormMixins
from .mixins.edit.messages import CreateMessageMixin, UpdateMessageMixin
from .mixins.edit.specific import SpecificCreateMixin

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
