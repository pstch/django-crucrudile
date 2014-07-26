"""A route is an implementation of the
:class:`django_crucrudile.entities.Entity` abstract class that yields
URL patterns made from its attributes. In the code, this is
represented by subclassing :class:`django_crucrudile.entity.Entity`
and providing a generator in ``patterns()``, yielding URL patterns
made from the route attributes. When route classes provide
:func:`django_crucrudile.entities.Entity.patterns`, it makes them
become concrete implementations of the Entity abstract class. Route
classes themselves are abstract by nature and need a definition of the
abstract function :func:`Route.get_callback`.

This module contains two abstract route classes (they are not usable
as such, but provide the base attributes and functions for route
objects) :

- :class:`Route` : the "main" abstract route class, provides
  :func:`Route.patterns`, yielding patterns made from the route
  metadata and using the callback returned by implementations of the
  abstract function :func:`Route.get_callback`.
- :class:`ModelRoute` : subclasses :class:`Route`, store model from
  arguments when instantiating, and provides functions to get route
  metadata from the model

These two abstract classes are used to provide three concrete
implementations, that take specific metadata (either on initialization
or as class attribute) to be able to return URL patterns :

- :class:`CallbackRoute` : Implements :class:`Route`, provides an
  implementation of :func:`Route.get_callback` that returns the
  callback set on the route (either in :func:`CallbackRoute.__init__`
  or as class attribute).
- :class:`ViewRoute` : Implements :class:`Route`, provides an
  implementation of :func:`Route.get_callback` that returns the a
  callback obtaining from the view class set on the route (either in
  :func:`ViewRoute.__init__` or as class attribute).
- :class:`ModelViewRoute` : Implements :class:`ModelRoute` using
  :class:`ViewRoute`, passes the model in the view keyword arguments,
  and can be used with Django generic views. Can also be used in a
  :class:`django_crucrudile.routers.ModelRouter` store.

"""

from .mixins import CallbackMixin, ViewMixin, ModelMixin, ArgumentsMixin
from .base import BaseRoute


class CallbackRoute(ArgumentsMixin, CallbackMixin, BaseRoute):
    pass


class ViewRoute(ArgumentsMixin, ViewMixin, BaseRoute):
    pass


class ModelViewRoute(ArgumentsMixin, ModelMixin, ViewMixin, BaseRoute):
    """Combine :class:`django_crucrudile.routes.mixins.ViewMixin` and
    :class:`django_crucrudile.routes.mixins.ModelMixin` to make a
    route that can easily be used with a model and a generic view.

    .. inheritance-diagram:: ModelViewRoute

    """
    def __init__(self, *args, **kwargs):
        # TODO: Experimental!
        super().__init__(*args, **kwargs)
        self.redirect = self.get_url_name() # Why ?

    def get_view_kwargs(self):
        """Make the view use :attr:`ModelRoute.model`.

        This is the effective combination of :class:`ModelRoute` and
        :class:`ViewRoute`.

        """
        return {'model': self.model}
