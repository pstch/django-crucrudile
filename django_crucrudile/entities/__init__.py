"""An entity is an abstract class of objects that can be used to make
an URL pattern tree.

.. seealso:: In ``django-crucrudile``, there are two classes that
             directly subclass :class:`Entity` :

              - :class:`django_crucrudile.routers.Router` (concrete)
              - :class:`django_crucrudile.routes.base.BaseRoute` (abstract)

"""
from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    """An entity is an abstract class of objects that can be used to make
an URL pattern tree.

    Abstract class that defines an attribute
    (:attr:`Entity.index`), and an abstract method
    (:func:`Entity.patterns`). Entity implementations should provide the
    :func:`Entity.patterns` method, that should return a generator
    yielding Django URL patterns.

    .. warning:: Abstract class ! Subclasses should define the
                 abstract :func:`patterns` method, that should return
                 a generator yielding Django URL objects
                 (:class:`django.core.urlresolvers.RegexURLPattern` or
                 `:class:`django.core.urlresolvers.RegexURLResolver`). See
                 warning in :func:`__init__`.


    .. inheritance-diagram:: Entity

    """
    index = False
    """
    :attribute index: Used when routed entity is registered, to know if
                      it should be registered as index.
    :type index: bool
    """
    def __init__(self, index=None):
        """Initialize entity, allow setting :attr:`index` from arguments, and
        add ``redirect`` instance attribute

        :argument index: See :attr:`index`
        """
        if index is not None:  # pragma: no cover
            self.index = index
        self.redirect = None

    @abstractmethod
    def patterns(self, parents=None,
                 add_redirect=None,
                 add_redirect_silent=None):  # pragma: no cover
        """Yield URL patterns

        .. note::

           For argument specification, see implementations of this
           abstract function (in particular
           :func:`django_crucrudile.routers.Router.patterns`)

        .. warning::

           Abstract method ! Should be defined by subclasses, and
           should return a generator yielding Django URL objects
           (``RegexURLPattern`` or ``RegexURLResolver``)

        """
        pass

    def get_str_tree(self, patterns_kwargs=None,
                     indent_char=' ', indent_size=2):
        """Return the representation of a entity patterns structure

        :argument patterns_kwargs: Keyword arguments to pass to
                                   :func:`patterns`
        :type patterns_kwargs: dict
        :argument indent_char: String to use for tree indentation
        :type indent_char: str
        :argument indent_size: Indent size
        :type indent_size: int

        >>> import tests.unit
        >>> from django.db.models import Model
        >>> from django_crucrudile.routers import Router, ModelRouter
        >>>
        >>> # needed to subclass Django Model
        >>> __name__ = "tests.doctests"
        >>>
        >>> class TestModel(Model):
        ...   pass

        >>> router = Router(generic=True)
        >>>
        >>> router.register(TestModel) is not None
        True

        >>> print(router.get_str_tree())
        ... # doctest: +NORMALIZE_WHITESPACE
         - Router  @ ^
           - GenericModelRouter testmodel @ ^testmodel/
             - testmodel-list-redirect @ ^$ RedirectView
             - testmodel-delete @ ^delete/(?P<pk>\d+)$ DeleteView
             - testmodel-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView
             - testmodel-update @ ^update/(?P<pk>\d+)$ UpdateView
             - testmodel-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
             - testmodel-create @ ^create$ CreateView
             - testmodel-detail @ ^detail/(?P<pk>\d+)$ DetailView
             - testmodel-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
             - testmodel-list @ ^list$ ListView

        """
        def _walk_tree(patterns, level=0):
            """Walk the tree, yielding at tuple of form :

            ``(level, namespace|router_class|model, callback)``

            """
            for pattern in patterns:

                callback = (
                    pattern.callback.__name__
                    if pattern.callback else None
                )

                if hasattr(pattern, 'url_patterns'):
                    # Resolver
                    # Yield a line with the resolver metadata
                    _model = getattr(pattern.router, 'model', None)
                    yield (
                        level,
                        pattern.namespace or
                        "{} {}".format(
                            pattern.router.__class__.__name__ or '',
                            _model._meta.model_name if _model else ''
                        ),
                        pattern.regex.pattern,
                        callback
                    )
                    # Then, yield lines with the pattern subpatterns
                    # (incrementing level)
                    for line_tuple in _walk_tree(
                            pattern.url_patterns, level+1):
                        yield line_tuple
                else:
                    # Pattern
                    # Yield a line with the pattern metadata
                    yield (
                        level,
                        pattern.name,
                        pattern.regex.pattern,
                        callback
                    )

        def _str_tree(lines):
            """Iterate over the tuple returned by _walk_tree, formatting it."""
            for _level, _name, _pattern, _callback in lines:
                yield "{} - {} @ {} {}".format(
                    indent_char*indent_size*_level,
                    _name or '',
                    _pattern or '',
                    _callback or '',
                )

        patterns_kwargs = patterns_kwargs or {}
        patterns = self.patterns(**patterns_kwargs)
        pattern_tuples = _walk_tree(patterns)
        pattern_lines = _str_tree(pattern_tuples)

        return '\n'.join(
            pattern_lines
        )
