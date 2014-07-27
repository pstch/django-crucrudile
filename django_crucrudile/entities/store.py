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

Doctests that use functionality in :class:`EntityStore` can be seen in
other classes (in particular
:class:`django_crucrudile.routers.Router`). They may help to get a
good idea of what the entity, entity store and entity graph concepts
mean.

"""
from abc import ABCMeta

__all__ = ['provides', 'EntityStoreMetaclass', 'EntityStore']


def provides(provided, **kwargs):
    """Return a decorator that uses :func:`EntityStore.register_class` to
    register the given object in the base store.

    :argument provided: Class (or object) to register in the base store. This
                        can be an object since it may be transformed
                        by :func:`EntityStore.register_apply_map`d
    :type provided: object

    """

    def register_obj_in_store(router):
        """Register the provided class to :argument:`store`

        :argument route: Router to register provided object to
        :type router: :class:`EntityStore`"""
        router.register_class(provided, **kwargs)
        return router
    return register_obj_in_store


class EntityStoreMetaclass(ABCMeta):
    """EntityStoreMetaclass allows :class:`EntityStore` to use a different
    :attr:`_base_store` store (list instance) for each class definitions
    (``cls`` instantiation)

    .. note::

       Subclasses :class:`abc.ABCMeta` because it will be used as the
       metaclass for an entity, and entity are abstract classes, which
       needs the :class:`âbc.ABCMeta` base class.

    .. inheritance-diagram:: EntityStoreMetaclass

    >>> class Store(metaclass=EntityStoreMetaclass):
    ...   pass
    >>>
    >>> class FailStore:
    ...   _fail_store = []
    >>>
    >>> class NewStore(Store):
    ...   pass
    >>>
    >>> class FailNewStore(FailStore):
    ...   pass

    >>> (NewStore._base_store is
    ...  Store._base_store)
    False
    >>> (NewStore._base_register_map is
    ...  Store._base_register_map)
    False
    >>> (NewStore._base_register_class_map is
    ...  Store._base_register_class_map)
    False

    >>> (FailNewStore._fail_store is
    ...  FailStore._fail_store)
    True

    """
    _base_store = []
    _base_register_map = {}
    _base_register_class_map = {}
    """
    :attribute _base_store: Routed entity class store, instantiated
                               upon Router instantiation.
    :type _base_store: list
    :attribute _base_register_map: Base register map (see
                                   :func:`get_register_map` and
                                   :func:`register`)
    :type _base_store: dict
    :attribute _base_register_class_map: Base register class map (see
                                         :func:`get_register_class_map`
                                         and :func:`register_class`)
    :type _base_store: dict
    """
    def __init__(cls, name, bases, attrs):
        """Replace :attr:`_base_store`, :attr:`_base_register_map` and
        :attr:`_base_register_class_map` by copies of themselves

        :argument name: New class name
        :type name: str
        :argument bases: New class bases
        :type bases: tuple
        :argument attrs: New class attributes
        :type attrs: dict

        .. seealso::

           For doctests that use this member, see
           :class:`django_crucrudile.entities.store.EntityStoreMetaclass`

        """
        super().__init__(name, bases, attrs)
        cls._base_register_map = cls._base_register_map.copy()
        cls._base_register_class_map = cls._base_register_class_map.copy()
        cls._base_store = cls._base_store.copy()


class EntityStore(metaclass=EntityStoreMetaclass):
    """Provides an entity store, and a :func:`register` method that
    registers entities in the entity store.

    The subclass implementation of :func:`patterns` should iterate over
    the entity store.

    .. inheritance-diagram:: EntityStore
    """
    def __init__(self):
        """Initialize router (create empty store and register base
        store)
        """
        super().__init__()
        self._store = []
        self.register_base_store()

    @staticmethod
    def register_apply_map(entity, mapping,
                           transform_kwargs=None, silent=True):
        """Apply mapping of value in ``mapping`` if ``entity`` is
        subclass (:func:`issubclass`) or instance (:func:`isinstance`) of key

        :argument entity: Object to pass to found mappings
        :type entity: object or class
        :argument mapping: Register mapping, used to get callable to
                           pass ``entity`` to
        :type mapping: dict
        :argument transform_kwargs: Extra keyword arguments to pass to
                                    the found transform functions
                                    (mapping keys)
        :type transform_kwargs: dict
        :argument silent: If set to ``False``, will fail if not
                          matching mapping was found.

        :raises LookupError: If ``silent`` is ``False``, and no
                             matching mapping was found

        >>> from mock import Mock
        >>>
        >>> class Class:
        ...   pass
        >>> class SubClass(Class):
        ...   pass
        >>> class OtherClass:
        ...   pass
        >>>
        >>> instance = SubClass()

        With instance :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   instance,
        ...   {Class: class_mock}
        ... )
        >>> class_mock.assert_called_once_with(instance)

        With instance, and default mapping :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   instance,
        ...   {None: class_mock}
        ... )
        >>> class_mock.assert_called_once_with(instance)

        With instance and iterable bases :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   instance,
        ...   {(OtherClass, Class): class_mock}
        ... )
        >>> class_mock.assert_called_once_with(instance)

        With instance and iterable bases (no matching base) :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   instance,
        ...   {(OtherClass, ): class_mock}
        ... )
        >>> applied is instance
        True
        >>> class_mock.called
        False

        With instance and iterable bases (no matching base, not
        silent) :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   instance,
        ...   {(OtherClass, ): class_mock},
        ...   silent=False
        ... )
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        LookupError: Could not find matching key in register
        mapping. Used test 'isinstance', register mapping bases are
        'OtherClass', tested against 'SubClass'

        With subclass :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   SubClass,
        ...   {Class: class_mock}
        ... )
        >>> class_mock.assert_called_once_with(SubClass)

        With subclass and iterable bases (no matching base) :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   SubClass,
        ...   {(OtherClass, ): class_mock}
        ... )
        >>> applied is SubClass
        True
        >>> class_mock.called
        False

        With subclass and single bases (no matching base, not silent) :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   SubClass,
        ...   {OtherClass: class_mock},
        ...   silent=False
        ... )
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        LookupError: Could not find matching key in register
        mapping. Used test 'issubclass', register mapping bases are
        'OtherClass', tested against 'SubClass'

        With subclass and no mappings (not silent) :

        >>> class_mock = Mock()
        >>> applied = EntityStore.register_apply_map(
        ...   SubClass,
        ...   {},
        ...   silent=False
        ... )
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        LookupError: Could not find matching key in register
        mapping. Used test 'issubclass', register mapping bases are
        '', tested against 'SubClass'

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
                    def _get_base_names():
                        for base, key in mapping.items():
                            if isinstance(base, tuple):
                                yield ', '.join(b.__name__ for b in base)
                            else:
                                yield base.__name__

                    raise LookupError(
                        "Could not find matching key in register mapping. "
                        "Used test '{}', register mapping bases are '{}', "
                        "tested against '{}'".format(
                            test.__name__,
                            ', '.join(_get_base_names()),
                            type(entity).__name__
                            if not isinstance(entity, type) else
                            entity.__name__
                        )
                    )
        if isinstance(entity, type):
            # entity is a class, test with issubclass
            return _find_entity(issubclass)
        else:
            # entity is not a class, test with isinstance
            return _find_entity(isinstance)

    @classmethod
    def get_register_class_map(self):
        """Mapping of type to function that will be evaluated (with entity)
        when calling register. See :func:`register_class` and
        :func:`register_apply_map`.

        Overriding implementations must call the base implementation
        (using super(), usually), so that the base mappings set by
        :func:`set_register_class_mapping` can be returned.

        The base implementation returns a copy of the stored mapping,
        so overriding implementations may append to the return value.

        .. seealso::

           For doctests that use this member, see
           :func:`django_crucrudile.entities.store.EntityStore.register_class`

        """
        return dict(self._base_register_class_map)

    @classmethod
    def get_register_class_map_kwargs(cls):
        """Arguments passed when applying register map, in
        :func:`register_class`

        .. seealso::

           For doctests that use this member, see
           :func:`django_crucrudile.entities.store.EntityStore.register_class`

        """
        return {}

    def get_register_map(self):
        """Mapping of type to function that will be evaluated (with entity)
        when calling register. See :func:`register` and
        :func:`register_apply_map`

        Overriding implementations *MUST* call the base implementation
        (using super(), usually), so that the base mappings set by
        :func:`set_register_mapping` can be returned.

        The base implementation returns a copy of the stored mapping,
        so overriding implementations may append to the return value.

        .. seealso::

           For doctests that use this member, see
           :func:`django_crucrudile.entities.store.EntityStore.register`

        """
        return dict(self._base_register_map)

    def get_register_map_kwargs(self):
        """Arguments passed when applying register map, in :func:`register`

        .. seealso::

           For doctests that use this member, see
           :func:`django_crucrudile.entities.store.EntityStore.register`

        """
        return self.get_register_class_map_kwargs()

    @classmethod
    def set_register_class_mapping(self, key, value):
        """Set a base register class mapping, that will be returned (possibly
        with other mappings) by :func:`get_register_class_map`.

        :argument key: Register class mapping bases
        :type key: class or tuple of classes
        :argument value: Register class mapping value
        :type value: callable

        >>> from mock import Mock
        >>> mock_mapping_func = Mock()
        >>>
        >>> class Class:
        ...   pass
        >>> class Store(EntityStore):
        ...   pass
        >>>
        >>>
        >>> Store.set_register_class_mapping(
        ...   Class, mock_mapping_func
        ... )
        >>> Store.get_register_class_map() == (
        ...   {Class: mock_mapping_func}
        ... )
        True
        """
        self._base_register_class_map[key] = value

    @classmethod
    def set_register_mapping(self, key, value):
        """Set a base register mapping, that will be returned (possibly
        with other mappings) by :func:`get_register_map`.

        :argument key: Register mapping bases
        :type key: class or tuple of classes
        :argument value: Register mapping value
        :type value: callable

        >>> from mock import Mock
        >>> mock_mapping_func = Mock()
        >>>
        >>> class Class:
        ...   pass
        >>>
        >>> class Store(EntityStore):
        ...   pass
        >>>
        >>> Store.set_register_mapping(
        ...   Class, mock_mapping_func
        ... )
        >>> Store().get_register_map() == (
        ...   {Class: mock_mapping_func}
        ... )
        True
        """
        self._base_register_map[key] = value

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

        :returns: The registered class, transformed by class register
                  mappings if there was a matching mapping
        :rtype: class

        >>> from mock import Mock
        >>> mock_entity_instance = Mock()
        >>> mock_entity = Mock()
        >>> mock_entity.side_effect = [mock_entity_instance]
        >>> mock_mapping_func = Mock()
        >>> mock_mapping_func.side_effect = [mock_entity]
        >>>
        >>> class Class:
        ...  pass
        >>>
        >>> class Store(EntityStore):
        ...   @classmethod
        ...   def get_register_class_map(self):
        ...     return {Class: mock_mapping_func}
        >>>
        >>> Store.register_class(Class) is mock_entity
        True
        >>>
        >>> Store._base_store == [mock_entity]
        True
        >>>
        >>> store = Store()
        >>> store._store == [mock_entity_instance]
        True
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
        return register_cls

    def register(self, entity, map_kwargs=None):
        """Register routed entity, applying mapping from
        :func:`get_register_map` where required

        :argument entity: Entity to register
        :type entity: :class:`django_crucrudile.entities.Entity`
        :argument map_kwargs: Argument to pass to mapping value if
                              entity gets transformed.
        :type map_kwargs: dict

        :returns: The registered entity, transformed by register
                  mappings if there was a matching mapping
        :rtype: :class:`django_crucrudile.entities.Entity`

        >>> from mock import Mock
        >>> mock_entity_instance = Mock()
        >>> mock_mapping_func = Mock()
        >>> mock_mapping_func.side_effect = [mock_entity_instance]
        >>>
        >>> class Class:
        ...  pass
        >>> instance = Class()
        >>>
        >>> class Store(EntityStore):
        ...   @classmethod
        ...   def get_register_map(self):
        ...     return {Class: mock_mapping_func}
        >>>
        >>> store = Store()
        >>> store.register(instance) == mock_entity_instance
        True
        >>> store._store == [mock_entity_instance]
        True
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

    def get_base_store_kwargs(self):
        """Arguments passed when instantiating entity classes in
        :attr:`_base_store`

        :returns: Keyword arguments
        :rtype: dict

        >>> from mock import Mock
        >>> mock_entity = Mock()
        >>>
        >>> class Store(EntityStore):
        ...   def get_base_store_kwargs(self):
        ...     return {'x': mock_entity}
        >>>
        >>> Store.register_class(lambda x: x) is not None
        True
        >>>
        >>> store = Store()
        >>> store._store == [mock_entity]
        True
        """
        return {}

    def register_base_store(self):
        """Instantiate entity classes in _base_store, using arguments from
        :func:`get_base_store_kwargs`

        >>> class Store(EntityStore):
        ...   pass
        >>>
        >>> Store.register_class(lambda: None) is not None
        True
        >>>
        >>> store = Store()
        >>> store._store
        [None]

        """
        kwargs = self.get_base_store_kwargs()
        for item in self._base_store:
            self.register(
                item(**kwargs),
            )
