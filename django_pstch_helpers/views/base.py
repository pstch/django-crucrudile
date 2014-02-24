"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import (View as DjangoView,
                                  TemplateView as DjangoTemplateView)

from .mixins.base import BaseMixins

class View(BaseMixins, DjangoView):
    """
    #TODO: Add class docstring
    """
    pass

class TemplateView(BaseMixins, DjangoTemplateView):
    """
    #TODO: Add class docstring
    """
    pass

class HomeView(TemplateView):
    """
    #TODO: Add class docstring
    """
    pass
