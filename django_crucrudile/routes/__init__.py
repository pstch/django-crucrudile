"""This module contains implementations of the
:class:`django_crucrudile.routes.base.BaseRoute` abstract class, that
use route mixins to provide functionality :

- :class:`CallbackRoute` provides a Route that needs a callback to be
  passed as argument or defined as
  :attr:`mixins.CallbackMixin.callback`
  attribute, and that uses this callback in the URL patterns it
  returns.
- :class:`ViewRoute` provides a Route that needs a view class to
  be passed as argument or defined as
  :attr:`mixins.ViewMixin.view_class`
  attribute, and that uses a callback obtained from this view class in the URL
  patterns it returns.
- :class:`ModelViewRoute` provides a Route that needs a view class and a
  model to be passed as arguments or defined as
  :attr:`mixins.ViewMixin.view_class` and
  :attr:`mixins.ModelMixin.model` attributes.
  attribute, that uses a callback obtained from this view class (using
  the model), and that uses this callback in the URL pattern it
  generates. Also uses metadata from the model class to generate some
  of the URL metadata.
- :class:`GenericModelViewRoute` provides a Route similar to
  :class:`ModelViewRoute`, but that automatically gets the needed URL
  arguments using the view class.

"""

from .mixins import (
    ArgumentsMixin,
    CallbackMixin, ViewMixin,
    ModelMixin, GenericViewArgsMixin,
)

from .base import BaseRoute

__all__ = [
    "CallbackRoute",
    "ViewRoute",
    "ModelViewRoute",
    "GenericModelViewRoute",
]


class CallbackRoute(ArgumentsMixin, CallbackMixin, BaseRoute):
    """Implement :class:`base.BaseRoute` using a
    callback function.

    Also use :class:`mixins.arguments.ArgumentsMixin`
    to allow URL arguments to be specified.


    .. inheritance-diagram:: CallbackRoute

    """
    def __init__(self, *args, **kwargs):
        """Initialize CallbackRoute, for a description of arguments see :

        - :func:`mixins.arguments.ArgumentsMixin.__init__`
        - :func:`mixins.callback.CallbackMixin.__init__`
        - :func:`base.BaseRoute.__init__`

        """
        super().__init__(*args, **kwargs)


class ViewRoute(ArgumentsMixin, ViewMixin, BaseRoute):
    """Implement :class:`base.BaseRoute` using a
    view class function.

    Also use :class:`mixins.arguments.ArgumentsMixin`
    to allow URL arguments to be specified.

    .. inheritance-diagram:: ViewRoute

    """
    def __init__(self, *args, **kwargs):  # pragma: no cover
        """Initialize ViewRoute, for a description of arguments see :

        - :func:`mixins.arguments.ArgumentsMixin.__init__`
        - :func:`mixins.view.ViewMixin.__init__`
        - :func:`base.BaseRoute.__init__`

        """
        super().__init__(*args, **kwargs)


class ModelViewRoute(ArgumentsMixin, ModelMixin, ViewMixin, BaseRoute):
    """Combine :class:`mixins.view.ViewMixin` and
    :class:`django_crucrudile.routes.mixins.model.ModelMixin` to make a
    route that can easily be used with a model and a generic view.

    Also use :class:`mixins.arguments.ArgumentsMixin`
    to allow URL arguments to be specified.

    .. inheritance-diagram:: ModelViewRoute

    """
    def __init__(self, *args, **kwargs):
        """Initialize ModelViewRoute, for a description of arguments see :

        - :func:`mixins.arguments.ArgumentsMixin.__init__`
        - :func:`mixins.model.ModelMixin.__init__`
        - :func:`mixins.view.ViewMixin.__init__`
        - :func:`base.BaseRoute.__init__`

        """
        super().__init__(*args, **kwargs)

    def get_view_kwargs(self):
        """Make the view use :attr:`mixins.model.ModelMixin.model`.

        This is the effective combination of
        :class:`mixins.model.ModelMixin` and :class:`ViewRoute`.

        >>> from mock import Mock
        >>>
        >>> model = Mock()
        >>> route = ModelViewRoute(model=model, view_class=Mock(),name='name')
        >>>
        >>> route.get_view_kwargs()['model'] is model
        True

        """
        return {'model': self.model}


class GenericModelViewRoute(GenericViewArgsMixin, ModelViewRoute):
    """Combine :class:`ModelViewRoute` with
:class:`django_crucrudile.routes.mixins.model.generic.GenericViewArgsMixin`
to automatically get the needed URL arguments for route instances.

    """
