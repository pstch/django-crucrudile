from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    """Abstract class for routed entities

    Subclasses should define the abstract :func:`patterns` method, that should
    return a generator yielding Django URL objects (``RegexURLPattern`` or
    ``RegexURLResolver``).


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
    def patterns(self, parents=None, add_redirect=True):
        """This abstract method should be defined by subclasses, as a
        generator that yields Django URL objects (``RegexURLPattern`` or
        ``RegexURLResolver``)

        """
        pass

    def get_str_tree(self, indent_char=' ', indent_size=2):
        """Return the representation of a entity patterns structure"""
        def _walk_tree(patterns, level=0):
            """Walk the tree, yielding at tuple of form :

            ``(level, namespace|router_class|model, callback)``

            """
            for pattern in patterns:
                try:
                    callback = (
                        pattern.callback.__name__
                        if pattern.callback else None
                    )
                except AttributeError:
                    callback = None

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
