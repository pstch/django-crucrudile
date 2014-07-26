from ..mixins.model import ModelMixin
from .. import Router

class ModelRouter(ModelMixin, Router):
    """Model router, implements
    :class:`django_crucrudile.routers.mixins.model.ModelMixin`with
    :class:`django_crucrudile.routers.Router`, to provide a Model that
    passes the model when instantiating entities.

    .. inheritance-diagram:: ModelRouter

    """
    pass
