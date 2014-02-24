"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import DjangoDetailView

from .mixins.base import BaseModelMixins

class DetailView(BaseModelMixins, DjangoDetailView):
    """
    #TODO: Add class docstring
    """
    pass

