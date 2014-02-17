from .detail import DetailableModelMixin
from .list import ListableModelMixin

from .edit.create import CreatableModelMixin, SpecificCreatableModelMixin
from .edit.update import UpdatableModelMixin
from .edit.delete import DeletableModelMixin

from .list.filtered import FiltedListableModelMixin

class BaseModelActionsMixin(DetailableModelMixin, ListableModelMixin):
    pass

class EditModelActionsMixin(CreatableModelMixin, UpdatableModelMixin, DeletableModelMixin):
    pass

class FullModelActionsMixin(BaseModelActionsMixin, EditModelActionsMixin):
    pass

__all__ = ['BaseModelActionsMixin', 'EditModelActionsMixin', 'FullModelActionsMixin',
           'ListableModelMixin', 'DetailableModelMixin', 'FilteredListableModelMixin',
           'CreatableModelMixin', 'SpecificCreatableModelMixin',
           'UpdatableModelMixin', 'DeletableModelMixin']
