"""The entity store class provides functions to register entity
instances in an entity store.

It also allow entity classes to be registered at class-level in a
"base store". These entity classes will be instantiated when the
entity store gets instantiated, and the resulting instances will be
registered.

It also allows "register mappings" to be defined, they allow objects
passed to register functions to be transformed based on a
mapping. When looking for a mapping, register functions will compare
their argument to the mapping key (using ``issubclass``, or
``isinstance``), and use the corresponding mapping value to get the
object that will be registered.

Additionally, register mapping keys can be iterables (list or tuples),
in which case the register functions will compare their argument to
any of the elements in the mapping key, and match even if only a
single item in the mapping key matches the argument.

The base store is copied on each class definition, using a metaclass,
so that using register functions that class-level won't alter the base
store of other class definitions.

This module also contains a :func:`provides` decorator, that
decorates a entity store class, adding an object to its base store.

"""
from functools import wraps
from abc import ABCMeta

__all__ = ['provides', 'EntityStoreMetaclass', 'EntityStore']


def provides(provided, **kwargs):
    """Return a decorator that uses :func:`EntityStore.register_class` to
    register the given object in the base store.

    :argument provided: Object to register in the base store. This
                        can be an object since it may be transformed
                        by register_class_map.
    :type provided: object

    """

    def register_obj_in_store(router):
        """Register the provided class to :argument:`store`

        :argument route: Router to register provided object to
        :type router: :class:`EntityStore`"""
        router.register_class(provided, **kwargs)
        return router
    return register_obj_in_store


def register_instances(to_store):
    """Return a decorator that makes all instances of this class (and its
    subclasses) automatically register themselves to :argument:`to_store`.

    :argument to_store: Store to register instances to.
    :type to_store: :class:`EntityStore`

    """
    def patch_constructor(entity_class):
        """Wrap original entity_class __init__, to register instance to
        :argument:`to_store`.

        """
        orig_init = entity_class.__init__

        @wraps(orig_init)
        def new_init(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            to_store.register(self)

        entity_class.__init__ = new_init
        return entity_class
    return patch_constructor


def register_class(to_store_class):
    """Return a decorator that registers the decorated class in the store
    class provided as argument, using :class:`EntityStore.register_class`.

    :argument to_store_class: Store class to register class to.
    :type to_store_class: subclass of :class:`EntityStore`

    """
    def register_obj_as_class(entity_class):
        """Register decorated class to :argument:`to_store_class`."""
        to_store_class.register_class(entity_class)
        return entity_class
    return register_obj_as_class


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
    def register_apply_map(entity, mapping,
                           transform_kwargs=None, silent=True):
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

        def _find_entity(test):
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
                            ', '.join(str(k) for k in mapping),
                            entity
                        )
                    )
        if not mapping:
            return entity
        elif isinstance(entity, type):
            # entity is a class, test with issubclass
            return _find_entity(issubclass)
        else:
            # entity is not a class, test with isinstance
            return _find_entity(isinstance)

    @classmethod
    def register_class(cls, register_cls, map_kwargs=None):
        """Add a route class to :attr:`_base_store`, appling mapping from
        :func:`get_register_class_map` where required. This route class will
        be instantiated (with kwargs from :func:`get_base_store_kwargs`)
        when the Router is itself instiated, using
        :func:`register_base_store`.

        :argument register_cls: Object to register (usually Route or
                                Router classes, but could be anything
                                because of possible mapping in
                                :func:`get_register_class_map_kwargs`)
        :argument map_kwargs: Argument to pass to mapping value if
                              entity gets transformed.
        :type map_kwargs: dict
        """
        register_class_map = cls.get_register_class_map()
        if register_class_map:
            if map_kwargs is None:
                map_kwargs = {}
            map_kwargs = dict(
                cls.get_register_class_map_kwargs(),
                **map_kwargs
            )

            register_cls = cls.register_apply_map(
                register_cls,
                register_class_map,
                map_kwargs
            )
        cls._base_store.append(register_cls)

    def register(self, entity, map_kwargs=None):
        """Register routed entity, applying mapping from
        :func:`get_register_map` where required

        :argument entity: Entity to register
        :type entity: :class:`django_crucrudile.entities.Entity`
        :argument map_kwargs: Argument to pass to mapping value if
                              entity gets transformed.
        :type map_kwargs: dict

        """
        register_map = self.get_register_map()
        if register_map:
            if map_kwargs is None:
                map_kwargs = {}
            map_kwargs = dict(
                self.get_register_map_kwargs(),
                **map_kwargs
            )

            entity = self.register_apply_map(
                entity,
                register_map,
                map_kwargs
            )
        self._store.append(entity)
        return entity

    @classmethod
    def get_register_class_map_kwargs(cls):
        """Arguments passed when applying register map, in
        :func:`register_class`"""
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
