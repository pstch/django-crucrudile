"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import DetailView as DjangoDetailView

from .mixins.base import BaseModelViewMixins

class DetailView(BaseModelViewMixins, DjangoDetailView):
    """
    #TODO: Add class docstring
    """
    pass

