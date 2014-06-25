from abc import ABCMeta, abstractmethod

from django.conf.urls import url, include


class RoutedEntity(metaclass=ABCMeta):
    """Abstract class for routed entities

    Subclasses should define the ``patterns()`` method, that should
    return a generator yielding Django URL objects (RegexURLPattern or
    RegexURLResolver).


    .. inheritance-diagram:: RoutedEntity
    """
    index = False
    """
    :attribute index: Used when routed entity is registered, to know if
                      it should be registered as index.
    :type index: bool
    """
    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        """This abstract method should be defined by subclasses, as a
        generator that yields Django URL objects (RegexURLPattern or
        RegexURLResolver)

        """
        pass

    def get_str_tree(self, indent_char=' ', indent_size=2):
        """Return the representation of a Router's patterns structure"""
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


class BaseRouterMetaclass(ABCMeta):
    """RouterMetaclass allows Router to use a different
    ``cls._base_store`` store (list instance) for each class definitions
    (``cls`` instantiation)

    .. inheritance-diagram:: BaseRouterMetaclass
    """
    _base_store = []
    """:attribute _base_store: Routed entity class store, instantiated
                               upon Router instantiation.
    :type _base_store: list
    """
    def __init__(cls, name, bases, attrs):
        """Replace ``cls._base_store`` by a copy of itself"""
        super().__init__(name, bases, attrs)
        cls._base_store = list(cls._base_store)


def provides(provided):
    def patch_router(router):
        router.register_class(provided)
        return router
    return patch_router


class BaseRouter(RoutedEntity, metaclass=BaseRouterMetaclass):
    _base_store = []
    """Base class for Routers

    Provides an entity store, and a ``register()`` method that
    registers entities in the entity store.

    The subclass implementation of ``patterns()`` should iterate over
    the entity store.

    .. inheritance-diagram:: BaseRouter
    """
    @property
    def register_map(self):
        """Mapping of type to function that will be evaluated (with entity)
        when calling register. See ``register_apply_map()``

        """
        return None

    def __init__(self):
        """Initialize router (create empty store and register base store)"""
        super().__init__()
        self._store = []
        self.register_base_store()

    @classmethod
    def register_class(self, cls):
        """Add a route class to _base_store. This route class will be
        instantiated (with kwargs from get_auto_register_kwargs())
        when the Router is itself instiated, using
        register_base_store()

        """
        self._base_store.append(cls)

    def get_auto_register_kwargs(self):
        """Arguments passed when instantiating entity classes in
        _base_store

        """
        return {}

    def register_base_store(self):
        """Instantiate entity classes in _base_store, using arguments from
        get_auto_register_kwargs()

        """
        kwargs = self.get_auto_register_kwargs()
        for item in self._base_store:
            self.register(
                item(**kwargs),
            )

    def register_apply_map(self, entity, transform_kwargs=None):
        """Apply mapping of value in ``self.register_map`` if entity is
        subclass (issubclass) or instance (isinstance) of key.

        """
        if transform_kwargs is None:
            transform_kwargs = {}

        def _match_entity(base, test):
            """Match the current entity against a given base,
            with a given test.

            """
            return base is None or test(entity, base)

        def _make_entity(func):
            """Make the new entity using the given function"""
            return func(
                entity,
                **transform_kwargs
            )

        def _find_entity(test, silent=True):
            """Find an entity matching the given test in register_map keys, then,
            with the matching value, return _make_entity(value).

            If no key matches, return original entity or fail with a
            LookupError if silent is False.

            """
            for base, func in self.register_map.items():
                if _match_entity(base, test):
                    # matching key, use value to make entity
                    return _make_entity(func)
            else:
                # not returned, so no match found
                if silent:
                    return entity
                else:
                    raise LookupError(
                        "Could not find matching key in register mapping. "
                        "Used test '{}', register mapping bases are '{}', "
                        "tested against '{}'".format(
                            test,
                            ', '.join(self.register_map.keys()),
                            entity
                        )
                    )

        if isinstance(entity, type):
            # entity is a class, test with issubclass
            return _find_entity(issubclass)
        else:
            # entity is not a class, test with isinstance
            return _find_entity(isinstance)

    def register(self, entity, index=False):
        """Register routed entity, applying mapping in ``register_map`` where
        required, and setting as index if ``index`` or ``entity.index`` is
        True.

        """
        if self.register_map:
            entity = self.register_apply_map(entity)
        self._store.append(entity)
        if index or entity.index:
            self.redirect = entity

class BaseRoute(RoutedEntity):
    name = None
    url_part = None
    auto_url_part = True

    def __init__(self, name=None, url_part=None):
        if name is not None:
            self.name = name
        elif self.name is None:
            raise Exception(
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
                raise Exception(
                    "No ``url_part`` argument provided to __init__"
                    ", and no url_part defined as class attribute."
                    " (in {})".format(self)
                )

    def patterns(self, *args, **kwargs):
        callback = self.get_callback()
        url_name = self.get_url_name()
        for url_part in self.get_url_parts():
            yield url(
                url_part,
                callback,
                url_name
            )

    @abstractmethod
    def get_callback(self):
        pass

    def get_url_parts(self):
        yield self.url_part

    def get_url_name(self):
        return self.name

class BaseViewRoute(BaseRoute):
    def __init__(self, view_class=None, name=None):
        super().__init__(name)
        if view_class is not None:
            self.view_class = view_class
        elif self.view_class is None:
            raise Exception(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )

class BaseModelRoute(BaseRoute):
    def __init__(self, model=None,
                 view_class=None, name=None):
        if model is not None:
            self.model = model
        elif self.model is None:
            raise Exception(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(view_class, name)


class BaseModelRouter(BaseRouter):
    """.. inheritance-diagram:: BaseModelRouter
    """
    model = None
    def get_auto_register_kwargs(self):
        """Add ModelRouter model to upstream auto register kwargs, so that the
        route classes in the base store will get the model as a kwarg when
        being instantiated.

        """
        kwargs = super().get_auto_register_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def __init__(self, model=None):
        # we need to set self.model before calling the superclass
        # __init__, because it will call
        # self.get_auto_register_kwargs() which needs self.model
        if model is not None:
            self.model = model
        elif self.model is None:
            raise Exception(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__()
