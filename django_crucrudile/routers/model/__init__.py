from ..mixins.model import ModelMixin
from .. import Router


class ModelRouter(ModelMixin, Router):
    """Model router, implements
    :class:`django_crucrudile.routers.mixins.model.ModelMixin`with
    :class:`django_crucrudile.routers.Router`, to provide a Model that
    passes the model when instantiating entities.

    .. inheritance-diagram:: ModelRouter

    >>> from django.views.generic.detail import SingleObjectMixin
    >>> from mock import Mock
    >>>
    >>> class GenericView(SingleObjectMixin):
    ...   pass
    >>> class NotGenericView:
    ...   pass

    >>> model = Mock()
    >>> view = Mock()
    >>>
    >>> model._meta.model_name = 'modelname'
    >>>
    >>> router = ModelRouter(model=model)
    >>>
    >>> router.model_url_part
    'modelname'

    >>> router.register(GenericView) is not None
    True

    """
    pass
