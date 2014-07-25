"""A route is an implementation of the abstract class Entity that
yields URL patterns made from its attributes. In the code, this is
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
from functools import partial
from abc import abstractmethod
from django.conf.urls import url

from django_crucrudile.entities import Entity
from django_crucrudile.urlutils import URLBuilder


__all__ = [
    'BaseRoute', 'Route',
    'CallbackRoute',
    'ViewRoute',
    'ModelRoute', 'ModelViewRoute'
]


class BaseRoute(Entity):
    """Abstract class for a :class:`django_crucrudile.entity.Entity` that
    yields URL patterns.

    .. warning:: Abstract class ! Subclasses should define the
                 :func:`get_callback` function.

    The URL part and URL name must be either set on class, or given at
    :func:`__init__`.

    .. inheritance-diagram:: Route
    """
    name = None
    """
    :attribute name: URL name to use for this pattern
    :type name: str
    """
    url_part = None
    """
    :attribute url_part: URL regex to use for the pattern
    :type url_part: str
    """
    auto_url_part = True
    """
    :attribute auto_url_part: Automatically set :attr:`url_part` to
                              :attr:`name` if set in class or passed
                              as :func:`__init__` argument.
    :type auto_url_part: bool
    """
    def __init__(self,
                 name=None, url_part=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
        defined.

        """
        if name is not None:
            self.name = name
        elif self.name is None:
            raise ValueError(
                "No ``name`` argument provided to __init__"
                ", and no name defined as class attribute."
                " (in {})".format(self)
            )
        if url_part is not None:
            self.url_part = url_part
        elif self.url_part is None:
            if self.auto_url_part:
                self.url_part = self.name
            else:
                raise ValueError(
                    "No ``url_part`` argument provided to __init__"
                    ", no url_part defined as class attribute."
                    " (in {}), and auto_url_part is set to False."
                    "".format(self)
                )
        super().__init__(**kwargs)

    def patterns(self, parents=None,
                 add_redirect=None,
                 add_redirect_silent=None):
        """Yield patterns for URL regexs in :func:`get_url_regexs`, using
        callback in :func:`get_callback` anpd URL name from
        :func:`get_url_name`.

        :argument parents: Not used in :class:`Route`'s implementation
                           of ``patterns``.
        :type parents: list of :class:`django_crucrudile.routers.Router`
        :argument add_redirect: Not used in :class:`Route`'s implementation
                                of ``patterns``.
        :type add_redirect: bool
        :argument add_redirect_silent: Not used in :class:`Route`'s
                                       implementation
                                       of ``patterns``.
        :type add_redirect_silent: bool

        """
        callback = self.get_callback()
        for regex in self.get_url_regexs():
            for name in self.get_url_names():
                yield url(
                    regex,
                    callback,
                    name=name
                )

    @abstractmethod
    def get_callback(self):  # pragma: no cover
        """Return callback to use in the URL pattern

        **Abstract method !** Should be defined by subclasses,
        otherwise class instantiation will fail.

        """
        pass

    def get_url_part(self):
        return self.url_part

    def get_url_parts(self):
        yield self.get_url_part()

    def get_url_specs(self):
        prefix = URLBuilder(None, '/')
        name = URLBuilder(None, '-')
        suffix = URLBuilder(None, '/', '/?')

        for part in self.get_url_parts():
            if part is not None:
                name.append(self.url_part)
            yield prefix, name, suffix

    def get_url_regexs(self):
        def _join_parts(iterable, join_str=''):
            return join_str.join(filter(None))
        for prefix, name, suffix in self.get_url_specs():
            _prefix, _name, _suffix = (
                part_list()
                for part_list in (prefix, name, suffix)
            )
            builder = URLBuilder([_prefix, _name, _suffix])
            required, built = builder()
            yield '^{}$'.format(built)

    def get_url_name(self):
        """Return the URL name, by default from :attr:`name`"""
        return self.name

    def get_url_names(self):
        yield self.get_url_name()

from .arguments import ArgumentsMixin

class Route(ArgumentsMixin, BaseRoute):
    pass


from .arguments import ArgumentsMixin
from .callback import CallbackRoute
from .view import ViewRoute
from .model import ModelRoute, ModelViewRoute
