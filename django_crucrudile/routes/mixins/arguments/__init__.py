"""This module contains the :class:`ArgumentsMixin` route mixin, that
uses :class:`parser.ArgumentsParser` to create a list of argument
combinations from the given argument list."""


from .parser import ArgumentsParser

__all__ = ["ArgumentsMixin", "ArgumentsParser"]


class ArgumentsMixin:
    """Route mixin, that builds the argument combination list when
    instantiating, and that yields (in :func:`get_url_specs`) another URL
    specification for each argument in resulting list.

    Should be a list that, if needed, contains argument
    specifications. An argument specification is a 2-tuple, contaning
    a boolean indicating if the argument is required or not,

    .. warning::

       This mixin does not make
       :class:`django_crucrudile.routes.base.BaseRoute` a concrete
       class !

    .. inheritance-diagram:: ArgumentsMixin

    """
    arguments_spec = None
    """
    :attribute arguments_spec: Argument list that will be passed to
                               :attr:`arguments_parser`. Should be
                               structured as the arguments parser
                               expects it.
    :type arguments_spec: list
    """
    arguments_parser = ArgumentsParser
    """
    :attribute arguments_parser: Argument parser to use to build the
                                 argument combinations from the
                                 argument specifications. Should be a
                                 :class:`django_crucrudile.urlutils.Parsable`
                                 subclass, or any class whose
                                 instances can be called to return its
                                 parsed output.
    :type arguments_parser: subclass of
                            :class:`django_crucrudile.urlutils.Parsable`
    """
    def __init__(self, *args,
                 arguments_spec=None,
                 **kwargs):
        """Initialize route, set arguments specification if given, and run
        arguments parser.

        :argument arguments_spec: See :attr:`arguments_spec`

        Example with the default test parser
        (:class:`parser.ArgumentsParser`) used with
        :class:`base.BaseRoute` :

        >>> from django_crucrudile.routes.base import BaseRoute
        >>>
        >>> class ArgumentsRoute(ArgumentsMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        >>>
        >>> route = ArgumentsRoute(
        ...   'name', 'url_part',
        ...   arguments_spec=[
        ...     ['<arg1.1>', '<arg1.2>'],
        ...     '<arg2>'
        ...   ]
        ... )
        >>>
        >>> list(route.get_url_regexs())
        ... # doctest: +NORMALIZE_WHITESPACE
        ['^url_part/<arg1.1>/<arg2>$',
         '^url_part/<arg1.2>/<arg2>$']

        """
        if arguments_spec is not None:
            self.arguments_spec = arguments_spec
        if self.arguments_spec is None:
            self.arguments_spec = []

        parser = self.arguments_parser(self.get_arguments_spec())
        self.arguments = parser()

        super().__init__(*args, **kwargs)

    def get_arguments_spec(self):
        """Yield argument specifications. By default, return specifications
        from :attr:`arguments_spec`. Subclasses or mixins may override this
        method to add their own argument specifications.

        :returns: Argument specifications
        :rtype: iterable

        >>> list(ArgumentsMixin().get_arguments_spec())
        []

        """
        for spec in self.arguments_spec:
            yield spec

    def get_url_specs(self):
        """Yield another URL specification for each argument in the argument
        combination list (arguments parser output).

        :returns: URL specifications
        :rtype: iterable of 3-tuple

        Example using the default test parser
        (:class:`parser.ArgumentsParser`) :

        >>> from django_crucrudile.routes.base import BaseRoute
        >>>
        >>> class ArgumentsRoute(ArgumentsMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        ...   arguments_spec=[
        ...     ['<arg1.1>', '<arg1.2>'],
        ...     '<arg2>'
        ...   ]
        >>>
        >>> route = ArgumentsRoute(
        ...   'name', 'url_part',
        ... )
        >>>
        >>> list(route.get_url_specs())
        ... # doctest: +NORMALIZE_WHITESPACE
        [([],
          ['url_part'],
          [(True, '<arg1.1>/<arg2>')]),
         ([],
          ['url_part'],
          [(True, '<arg1.2>/<arg2>')])]

        """
        for prefix, name, suffix in super().get_url_specs():
            if self.arguments:
                for arg in self.arguments:
                    yield prefix, name, suffix + [arg]
            else:
                yield prefix, name, suffix
