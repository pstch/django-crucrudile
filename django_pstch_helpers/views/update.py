"""
#TODO: Add module docstring
"""
#pylint: disable=R0901,R0904

from django.views.generic import UpdateView as DjangoUpdateView

from .mixins.base import BaseModelFormMixins

from .mixins.edit.messages import UpdateMessageMixin

class UpdateView(BaseModelFormMixins, UpdateMessageMixin, DjangoUpdateView):
    """
    #TODO: Add class docstring
    """
    pass

