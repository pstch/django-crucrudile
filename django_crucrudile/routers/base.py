from abc import ABCMeta, abstractmethod, abstractproperty


class RoutedEntity(metaclass=ABCMeta):
    """Abstract class for routed entities

    Subclasses should define the ``patterns()`` method, that should
    return a generator yielding Django URL objects (RegexURLPattern or
    RegexURLResolver).

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


class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class BaseRouterMetaclass(ABCMeta):
    """RouterMetaclass allows Router to use a different
    ``cls._base_store`` store (list instance) for each class definitions
    (``cls`` instantiation)

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

    """
    register_map = None
    """
    :attribute register_map: Mapping of type to function that will be
                             evaluated (with entity) when calling
                             register. See ``register_apply_map()``
    :type register_map: dict
    """
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
        instance or subclass of key

        """
        if self.register_map:
            transform_kwargs = transform_kwargs or {}
            for base, func in self.register_map.items():
                if (base is None or  # None matches all keys
                    isinstance(entity, base) or  # is instance of key
                    (isinstance(entity, type) and  # is class
                     issubclass(entity, base))):  # is subclass of key
                    return func(entity, **transform_kwargs)
            else:
                raise TypeError(
                    "A register transform mapping is defined, but could "
                    "not find a matching mapping for {}".format(entity)
                )
        else:
            return entity

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


class BaseModelRouter(BaseRouter):
    def __init__(self, *args, **kwargs):
        model = kwargs['model']
        self.model = model
        super().__init__(args, kwargs)

    def get_auto_register_kwargs(self):
        kwargs = super().get_auto_register_kwargs()
        kwargs['model'] = self.model
        return kwargs
