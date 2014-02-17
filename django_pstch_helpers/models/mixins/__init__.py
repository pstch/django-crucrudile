from .base import DetailableModelMixin, ListableModelMixin
from .edit import CreatableModelMixin, UpdatableModelMixin, DeletableModelMixin

class BaseModelActionsMixin(DetailableModelMixin, ListableModelMixin):
    pass

class EditModelActionsMixin(CreatableModelMixin, UpdatableModelMixin, DeletableModelMixin):
    pass

class FullModelActionsMixin(BaseModelActionsMixin, EditModelActionsMixin):
    pass
