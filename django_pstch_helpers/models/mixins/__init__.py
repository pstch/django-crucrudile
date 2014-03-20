"""
#TODO: Add module docstring
"""
#pylint: disable=F0401
from .base import ModelInfoMixin, AutoPatternsMixin

from .detail import DetailableModelMixin

from .list import ListableModelMixin
from .list.filtered import FilteredListableModelMixin

from .edit import (CreatableModelMixin,
                   SpecificCreatableModelMixin,
                   UpdatableModelMixin,
                   DeletableModelMixin)

#pylint: enable=F0401

#pylint: disable=R0901,R0903,W0232

class BaseModelActionsMixin(DetailableModelMixin,
                            ListableModelMixin):
    """
    #TODO: Add class docstring
    """
    pass

class EditModelActionsMixin(CreatableModelMixin,
                            UpdatableModelMixin,
                            DeletableModelMixin):
    """
    #TODO: Add class docstring
    """
    pass

class FullModelActionsMixin(BaseModelActionsMixin,
                            EditModelActionsMixin):
    """
    #TODO: Add class docstring
    """
    pass

__all__ = ['ModelInfoMixin', 'AutoPatternsMixin',
           'BaseModelActionsMixin', 'EditModelActionsMixin',
           'FullModelActionsMixin',
           'ListableModelMixin', 'DetailableModelMixin',
           'FilteredListableModelMixin',
           'CreatableModelMixin', 'SpecificCreatableModelMixin',
           'UpdatableModelMixin', 'DeletableModelMixin']
