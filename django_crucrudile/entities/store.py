from abc import ABCMeta

__all__ = ['provides', 'EntityStoreMetaclass', 'EntityStore']


def provides(provided, **kwargs):
    """Return a decorator that uses :func:`EntityStore.register_class` to
    register a class in the base store
    """

    def register_class_to_router(router):
        """Register the provided class"""
        router.register_class(provided, **kwargs)
        return router
    return register_class_to_router


class EntityStoreMetaclass(ABCMeta):
    """EntityStoreMetaclass allows :class:`EntityStore` to use a different
    :attr:`_base_store` store (list instance) for each class definitions
    (``cls`` instantiation)

    .. inheritance-diagram:: EntityStoreMetaclass
    """
    _base_store = []
    """:attribute _base_store: Routed entity class store, instantiated
                               upon Router instantiation.
    :type _base_store: list
    """
    def __init__(cls, name, bases, attrs):
        """Replace :attr:`_base_store` by a copy of itself"""
        super().__init__(name, bases, attrs)
        cls._base_store = list(cls._base_store)


class EntityStore(metaclass=EntityStoreMetaclass):
    """Provides an entity store, and a :func:`register` method that
    registers entities in the entity store.

    The subclass implementation of :func:`patterns` should iterate over
    the entity store.

    .. inheritance-diagram:: EntityStore
    """
    _base_store = []
    """
    :attribute _base_store: Empty store, mutable list, but will be
                            copied for each type instance by
                            :class:`EntityStoreMetaclass`
    :type _base_store: list
    """
    def get_register_map(self):
        """Mapping of type to function that will be evaluated (with entity)
        when calling register. See :func:`register` and
        :func:`register_apply_map`

        """
        return {}

    @classmethod
    def get_register_class_map(self):
        """Mapping of type to function that will be evaluated (with entity)
        when calling register. See :func:`register_class` and
        :func:`register_apply_map`

        """
        return {}

    def __init__(self):
        """Initialize router (create empty store and register base store)"""
        super().__init__()
        self._store = []
        self.register_base_store()

    @staticmethod
    def register_apply_map(entity, mapping, transform_kwargs=None):
        """Apply mapping of value in ``mapping`` if ``entity`` is
        subclass (``issubclass``) or instance (``isinstance``) of key

        """
        if transform_kwargs is None:
            transform_kwargs = {}

        def _match_entity(base, test):
            """Match the current entity against a given base,
            with a given test

            """
            if base is None:
                return True
            elif isinstance(base, (list, tuple)):
                return any(
                    test(entity, _base)
                    for _base in base
                )
            else:
                return test(entity, base)

        def _make_entity(func):
            """Make the new entity using the given function"""
            return func(
                entity,
                **transform_kwargs
            )

        def _find_entity(test, silent=True):
            """Find an entity matching the given test in register_map keys, then,
            with the matching value, return :func:`_make_entity(value)`.

            If no key matches, return original entity or fail with a
            ``LookupError`` if silent is False.

            """
            for base, func in mapping.items():
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
                            ', '.join(mapping.keys()),
                            entity
                        )
                    )

        if isinstance(entity, type):
            # entity is a class, test with issubclass
            return _find_entity(issubclass)
        else:
            # entity is not a class, test with isinstance
            return _find_entity(isinstance)

    @classmethod
    def register_class(cls, register_cls, **kwargs):
        """Add a route class to :attr:`_base_store`, appling mapping from
        :func:`get_register_class_map` where required. This route class will
        be instantiated (with kwargs from :func:`get_base_store_kwargs`)
        when the Router is itself instiated, using
        :func:`register_base_store`.

        """
        register_class_map = cls.get_register_class_map()
        if register_class_map:
            register_kwargs = cls.get_register_class_map_kwargs()
            register_kwargs.update(kwargs)

            register_cls = cls.register_apply_map(
                register_cls,
                register_class_map,
                register_kwargs
            )
        cls._base_store.append(register_cls)

    def register(self, entity):
        """Register routed entity, applying mapping from :func:`get_register_map` where
        required

        """
        register_map = self.get_register_map()
        if register_map:
            kwargs = self.get_register_map_kwargs()
            entity = self.register_apply_map(
                entity,
                register_map,
                kwargs
            )
        self._store.append(entity)
        return entity

    @classmethod
    def get_register_class_map_kwargs(cls):
        """Arguments passed when applying register map, in :func:`register_class`"""
        return {}

    def get_register_map_kwargs(self):
        """Arguments passed when applying register map, in :func:`register`"""
        return self.get_register_class_map_kwargs()

    def get_base_store_kwargs(self):
        """Arguments passed when instantiating entity classes in
        :attr:`_base_store`

        """
        return {}

    def register_base_store(self):
        """Instantiate entity classes in _base_store, using arguments from
        :func:`get_base_store_kwargs`

        """
        kwargs = self.get_base_store_kwargs()
        for item in self._base_store:
            self.register(
                item(**kwargs),
            )
