from .base import ModelInfoMixin, AutoPatternsMixin

from .detail import DetailableModelMixin

from .list import ListableModelMixin
from .list.filtered import FilteredListableModelMixin

from .edit import CreatableModelMixin, SpecificCreatableModelMixin, UpdatableModelMixin
from .delete import DeletableModelMixin

class BaseModelActionsMixin(DetailableModelMixin,
                            ListableModelMixin):
    pass

class EditModelActionsMixin(CreatableModelMixin,
                            UpdatableModelMixin,
                            DeletableModelMixin):
    pass

class FullModelActionsMixin(BaseModelActionsMixin,
                            EditModelActionsMixin):
    pass

__all__ = ['ModelInfoMixin', 'AutoPatternsMixin',
           'BaseModelActionsMixin', 'EditModelActionsMixin',
           'FullModelActionsMixin',
           'ListableModelMixin', 'DetailableModelMixin',
           'FilteredListableModelMixin',
           'CreatableModelMixin', 'SpecificCreatableModelMixin',
           'UpdatableModelMixin', 'DeletableModelMixin']
