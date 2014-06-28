"""An entity is an abstract class that defines an attribute
(:attr:`Entity.index`), and an abstract method
(:func:`Entity.patterns`). Entity implementations should provide the
:func:`Entity.patterns` method, that should return a generator
yielding Django URL patterns.

.. seealso:: In ``django-crucrudile``, there are two classes that
             directly subclass :class:`Entity` :

              - :class:`django_crucrudile.routers.Router`
              - :class:`django_crucrudile.routes.Route`

"""
from abc import ABCMeta, abstractmethod

from django.core.urlresolvers import RegexURLPattern


class Entity(metaclass=ABCMeta):
    """Abstract class for routed entities

    .. warning:: Abstract class ! Subclasses should define the
                 abstract :func:`patterns` method, that should return
                 a generator yielding Django URL objects
                 (``RegexURLPattern`` or ``RegexURLResolver``).


    .. inheritance-diagram:: Entity
    """
    index = False
    """
    :attribute index: Used when routed entity is registered, to know if
                      it should be registered as index.
    :type index: bool
    """
    def __init__(self, index=None):
        if index is not None:
            self.index = index

    @abstractmethod
    def patterns(self, parents=None, add_redirect=True):  # pragma: no cover
        """Yield URL patterns

        .. warning:: This abstract method should be defined by
                     subclasses, and should return a generator
                     yielding Django URL objects (``RegexURLPattern``
                     or ``RegexURLResolver``)

        """
        pass

    def get_str_tree(self, indent_char=' ', indent_size=2):
        """Return the representation of a entity patterns structure"""
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

        patterns = self.patterns()
        pattern_tuples = _walk_tree(patterns)
        pattern_lines = _str_tree(pattern_tuples)

        return '\n'.join(
            pattern_lines
        )

    def get_pydot_graph(self, recurse_limit=None):
        """Unmaintained at the time. Returns a graph of the patterns and
        subpatterns, made using pydot.

        .. note:: Requires ``pydot`` (a version compatible with the
                     current Python interpreter) to be installed.


        """
        import pydot
        _graph = pydot.Dot(graph_type='graph')

        def pattern_add_edges(graph, pattern,
                              recursive=False, recurse_limit=None):
            def get_node(_pattern):
                if getattr(_pattern, 'namespace', None) is not None:
                    color = 'green'
                elif isinstance(_pattern, RegexURLPattern):
                    color = 'red'
                else:
                    color = 'blue'

                node = pydot.Node(
                    str(id(_pattern)),
                    style="filled",
                    fillcolor=color
                )

                namespace = getattr(_pattern, 'namespace', None)
                name = getattr(_pattern, 'name', None)
                callback = getattr(_pattern, 'callback', None)
                redirect_url = getattr(_pattern, '_redirect_url_name', None)
                router = getattr(_pattern, 'router', None)
                model = getattr(router, 'model', None)
                regex = getattr(_pattern, 'regex', None)
                regex_pattern = regex.pattern if regex else None

                node.set_label(
                    '\n'.join(filter(None, [
                        'namespace is {}'.format(namespace)
                        if namespace else None,
                        'callback is {}'.format(callback.__name__)
                        if callback else None,
                        'redirect_url is {}'.format(redirect_url)
                        if redirect_url else None,
                        'router is {}'.format(router.__class__.__name__)
                        if router else None,
                        'model is {}'.format(model._meta.model_name)
                        if model else None,
                        'URL part is {}'.format(regex_pattern)
                        if regex_pattern else None,
                        'URL name is {}'.format(name)
                        if name else None,
                    ]))
                )

                return node

            pattern_node = get_node(pattern)
            graph.add_node(pattern_node)

            for sub_pattern in getattr(pattern, 'url_patterns', []):
                node = get_node(sub_pattern)

                edge = pydot.Edge(
                    pattern_node,
                    node,
                )

                graph.add_edge(edge)

                if recursive and recurse_limit != 0:
                    if recurse_limit is not None:
                        recurse_limit -= 1
                    pattern_add_edges(
                        graph,
                        sub_pattern,
                        recursive, recurse_limit
                    )

        for pattern in self.patterns():
            pattern_add_edges(
                _graph, pattern,
                True, recurse_limit
            )

        return _graph
