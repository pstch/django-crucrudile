"""
#TODO: Add module docstring
"""
#pylint: disable=R0901, R0904
from django.views.generic import (View as DjangoView,
                                  TemplateView as DjangoTemplateView)

from .mixins.base import BaseMixins

class View(BaseViewMixins, DjangoView):
    """
    #TODO: Add class docstring
    """
    def get_action_name
    pass

class TemplateView(BaseViewMixins, DjangoTemplateView):
    """
    #TODO: Add class docstring
    """
    pass

class HomeView(TemplateView):
    """
    #TODO: Add class docstring
    """
    pass
