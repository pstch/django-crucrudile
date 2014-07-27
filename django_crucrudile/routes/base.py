"""This module contains the "main" abstract route class, that provides
:func:`BaseRoute.patterns`, yielding patterns made from the route
metadata and using the callback returned by implementations of the
abstract function :func:`BaseRoute.get_callback`.

.. note::

   This route class is one the two (along with
   :class:`django_crucrudile.routers.Router`) standard implementations
   of the :class:`django_crucrudile.entities.Entity` abstract class.

"""
from itertools import product
from abc import abstractmethod
from django.conf.urls import url

from django_crucrudile.entities import Entity
from django_crucrudile.urlutils import URLBuilder


class BaseRoute(Entity):
    """Abstract class for a :class:`django_crucrudile.entities.Entity`
    that URL patterns that point to its implementation of
    :func:`get_callback`. Implements
    :func:`django_crucrudile.entities.Entity.patterns` using
    :func:`patterns`.

    .. warning::

       Abstract class ! Subclasses should define the
       :func:`get_callback` function. See warning in :func:`__init__`.

    The URL part and URL name must be either set on class, or given at
    :func:`__init__`.

    .. inheritance-diagram:: BaseRoute

    """
    name = None
    """
    :attribute name: URL name to use for this pattern (will be used
                     for the Django URL pattern name)
    :type name: str
    """
    url_part = None
    """
    :attribute url_part: URL regex to use for the pattern (will be
                         used in the URL regexp)
    :type url_part: str
    """
    auto_url_part = True
    """
    :attribute auto_url_part: Automatically set :attr:`url_part` to
                              :attr:`name` if none defined.
    :type auto_url_part: bool

    """
    def __init__(self,
                 name=None, url_part=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
        defined.

        Also sets ``self.redirect`` to the URL name (using
        :func:`get_url_name`).

        :argument name: See :attr:`name`
        :argument url_part: See :attr:`url_part`

        :raises ValueError: If :attr:`name` is ``None``, and not given in
                            args
        :raises ValueError: If :attr:`url_part` is ``None``, and not given
                            in args, and :attr:`auto_url_part` is ``None``
                            or :attr:`name` is ``None``
        :raises TypeError: If :func:`get_callback` not implemented
                           (see warning below)

        .. warning ::

           This method cannot be called on :class:`BaseRoute`, as
           it is an abstract class missing an implementation of
           :func:`get_callback` :


           >>> try:
           ...   BaseRoute()
           ... except Exception as catched:
           ...   type(catched).__name__
           ...   str(catched) == (
           ...     "Can't instantiate abstract class BaseRoute "
           ...     "with abstract methods get_callback"
           ...   )
           'TypeError'
           True

        """
        if name is not None:
            self.name = name
        elif self.name is None:
            raise ValueError(
                "No ``name`` argument provided to __init__"
                ", and no :attr:`name` defined as class attribute."
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
                    ", no :attr:`url_part` defined as class attribute."
                    " (in {}), and :attr:`auto_url_part` is set to False."
                    "".format(self)
                )
        super().__init__(**kwargs)
        self.redirect = self.get_url_name()

    def patterns(self, parents=None,
                 add_redirect=None,
                 add_redirect_silent=None):
        """Yield patterns for URL regexs in :func:`get_url_regexs`, using
        callback in :func:`get_callback` and URL name from
        :func:`get_url_name`.

        :argument parents: Not used in :class:`BaseRoute`'s implementation
                           of ``patterns``.
        :type parents: list of :class:`django_crucrudile.routers.Router`
        :argument add_redirect: Not used in :class:`BaseRoute`'s implementation
                                of ``patterns``.
        :type add_redirect: bool
        :argument add_redirect_silent: Not used in :class:`BaseRoute`'s
                                       implementation
                                       of ``patterns``.
        :type add_redirect_silent: bool

        :returns: Django URL patterns
        :rtype: iterable of ``RegexURLPattern``

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> list(route.patterns())
        [<RegexURLPattern name ^url_part$>]

        """
        callback = self.get_callback()

        regexs_names = product(
            self.get_url_regexs(),
            self.get_url_names()
        )

        for regex, name in regexs_names:
                yield url(
                    regex,
                    callback,
                    name=name
                )

    @abstractmethod
    def get_callback(self):  # pragma: no cover
        """Return callback to use in the URL pattern

        .. warning::

           Abstract method ! Should be implemented in subclasses,
           otherwise class instantiation will fail. See warning in
           :func:`__init__`.

        :returns: Callable to use in the URL patter
        :rtype: callable

        """
        pass

    def get_url_name(self):
        """Get the main URL name, defined at class level (:attr:`name`) or
        passed to :func:`__init__`.

        :returns: main URL name
        :rtype: str

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> route.get_url_name()
        'name'

        """
        return self.name

    def get_url_names(self):
        """Get a list of URL names to generate patterns for. An least one URL
        pattern will be returned for each URL name returned by this
        function.

        The default implementation returns a singleton (:func:`get_url_name`).

        :returns: URL names (list of URL name)
        :rtype: iterable of str

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> print(list(route.get_url_names()))
        ['name']

        """
        yield self.get_url_name()

    def get_url_part(self):
        """Get the main URL part, defined at class level (:attr:`url_part`) or
        passed to :func:`__init__`.

        :returns: main URL part
        :rtype: str

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> route.get_url_part()
        'url_part'

        """
        return self.url_part

    def get_url_parts(self):
        """Get a list of URL parts to generate patterns for. At least one URL
        pattern will be returned for each URL part returned by this
        function.

        The default implementation returns a singleton (:func:`get_url_part`).

        :returns: URL parts (list of URL part)
        :rtype: iterable of str

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> list(route.get_url_parts())
        ['url_part']

        """
        yield self.get_url_part()

    def get_url_specs(self):
        """Yield URL specifications. An URL specification is a 3-tuple,
        containing 3 :class:`django_crucrudile.urlutils.URLBuilder` instances :
        ``prefix``, ``name`` and ``suffix``. These objects are used to
        join together different part of the URLs. Using them in a
        3-tuple allows building an URL part with a "central" name,
        (whose parts are joined using ``-``), a prefix (joined using
        ``/``), and a suffix (joined using ``/``, ``/?``). This schema
        allows different subclasses to register different parts in the
        URLs (without interfering with each other, using
        :func:`super()`), and provides automatic optional/required
        separator handling.

        The base implementation yields a specification for each URL
        part returned by :func:`get_url_parts`.

        .. note::

           The ``prefix``, ``name`` and ``suffix`` names for the URL
           specification contents are purely indicative, and never
           used as identifiers. They are used in this package's code
           for consistency.

        :returns: URL specifications
        :rtype: iterable of 3-tuple

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> list(route.get_url_specs())
        [([], ['url_part'], [])]

        """
        prefix = URLBuilder(None, '/')
        name = URLBuilder(None, '-')
        suffix = URLBuilder(None, '/', '/?')

        for part in self.get_url_parts():
            if part is not None:
                name.append(self.url_part)
            yield prefix, name, suffix

    def get_url_regexs(self):
        """Yield URL regexs to generate patterns for.

        For each URL specification in :func:`get_url_specs` :

        - Run each :class:`django_crucrudile.urlutils.URLBuilder`
          instance in the URL specification 3-tuple (``prefix``,
          ``name`` and ``suffix``)
        - Pass builder outputs in another URL builder
        - Run this builder, and yield output, prefixed with '^' and
          suffixed with '$'

        URL specifications are structured as follow :

        - iterable (list of
        - iterable (3-tuple) of
        - iterable (URLBuilder) of
        - URL part

        We use :class:`django_crucrudile.urlutils.URLBuilder` twice,
        first to join the URL parts in each URL builder of the
        specification (``prefix``, ``name`` and ``suffix``), and then
        to join together the 3 resulting URL parts.

        It's not possible to flatten this list directly, because
        ``prefix``, ``name`` and ``suffix`` may use different
        separators.

        :returns: URL regexs
        :rtype: iterable of string

        >>> class Route(BaseRoute):
        ...   def get_callback(self):
        ...    pass
        >>>
        >>> route = Route('name', 'url_part')
        >>> list(route.get_url_regexs())
        ['^url_part$']

        """
        for prefix, name, suffix in self.get_url_specs():
            _prefix, _name, _suffix = (
                part_list()
                for part_list in (prefix, name, suffix)
            )
            builder = URLBuilder([_prefix, _name, _suffix])
            required, built = builder()
            yield '^{}$'.format(built)
