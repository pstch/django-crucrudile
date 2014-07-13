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
from functools import lru_cache
from abc import abstractmethod
from django.conf.urls import url

from django_crucrudile.entities import Entity

from .arguments import RouteArguments

__all__ = [
    'Route',
    'CallbackRoute',
    'ViewRoute',
    'ModelRoute', 'ModelViewRoute'
]


class ArgumentsMixin:
    _argument_obj = None
    arguments_spec = []
    arguments_parsers = RouteArguments

    def __init__(self,
                 arguments_spec=None, arguments_class=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
defined.

        """
        if arguments_spec is not None:
            self.arguments_spec = arguments_spec
        if arguments_class is not None:
            self.arguments_class = arguments_class

        self.arguments = self.arguments_spec

        super().__init__(**kwargs)

    @property
    def arguments(self):
        return self._argument_obj

    @arguments.setter
    def arguments(self, arguments):
        self._argument_obj = self._get_argument_obj(
            arguments, self.arguments_class
        )

    @staticmethod
    def _get_argument_obj(arguments, arguments_class):
        is_arguments_class = isinstance(
            arguments,
            arguments_class
        )
        if is_arguments_class:
            arguments
        elif arguments_class.test_input(arguments):
            return arguments_class(arguments)
        else:
            raise TypeError("Could not parse arguments : {}".format(arguments))

    def get_arg_regexs(self):
        regexs = self.arguments.arg_combs
        separator = self.arguments.get_separator()
        for regex in regexs:
            yield separator, regex

    def clean_url_part(self, url_part=None):
        if url_part is not None:
            part = url_part
        else:
            part = self.url_part
        if part:
            return '/' + part
        else:
            return ''

    def make_url_regexs(self, url_part=None):
        part = self.clean_url_part(url_part)
        for arg in self.arguments.arg_combs:
            yield '^{}$'.format(
                self.arguments.get_separator().join(
                    filter(None, [part, arg])
                    )
                )

class Route(Entity):
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
        for url_regex in self.get_url_regexs():
            for url_name in self.make_url_names():
                yield url(
                    url_regex,
                    callback,
                    name=url_name
                )

    @abstractmethod
    def get_callback(self):  # pragma: no cover
        """Return callback to use in the URL pattern

        **Abstract method !** Should be defined by subclasses,
        otherwise class instantiation will fail.

        """
        pass

    def make_url_regexs(self, url_part=None):
        if url_part is not None:
            part = url_part
        else:
            part = self.url_part
        if part:
            yield '/' + part
        else:
            yield ''

    def make_url_names(self):
        """Return the URL name, by default from :attr:`name`"""
        yield self.name

    def get_url_regexs(self, url_part=None):
        """Yield URL parts (for different combinations of URL
        arguments). The :class:`Route` bimplementation of
        :func:`patterns` will yield an URL pattern for each URL regex
        returned by this iterator.

        By default, yields only :attr:`url_part`.
        """
        for url_regex in self.make_url_regexs():
            yield url_regex


from .callback import CallbackRoute
from .view import ViewRoute
from .model import ModelRoute, ModelViewRoute
