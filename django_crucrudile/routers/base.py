from itertools import chain

from abc import ABCMeta

from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from django.views.generic import RedirectView

from django_crucrudile.entity import RoutedEntity


class EntityStoreMetaclass(ABCMeta):
    """EntityStoreMetaclass allows Router to use a different
    ``cls._base_store`` store (list instance) for each class definitions
    (``cls`` instantiation)

    .. inheritance-diagram:: EntityStoreMetaclass
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


class EntityStore(metaclass=EntityStoreMetaclass):
    _base_store = []
    """Base class for Routers

    Provides an entity store, and a ``register()`` method that
    registers entities in the entity store.

    The subclass implementation of ``patterns()`` should iterate over
    the entity store.

    .. inheritance-diagram:: EntityStore
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

    def register(self, entity):
        """Register routed entity, applying mapping in ``register_map`` where
        required.

        """
        if self.register_map:
            entity = self.register_apply_map(entity)
        self._store.append(entity)
        return entity


class BaseRouter(EntityStore, RoutedEntity):
    label = None
    namespace = None
    url_part = None
    redirect = None

    def __init__(self, name=None, label=None,
                 namespace=None, url_part=None,
                 redirect=None):
        """Initialize Router base attributes, initialize entity store _store,
        and instantiate entities from entity classes in _base_store

        """
        # initialize base attributes
        if label is not None:
            self.label = label
        if namespace is not None:
            self.namespace = namespace
        if url_part is not None:
            self.url_part = url_part
        if redirect is not None:
            self.redirect = redirect

        # call superclass implementation of __init__
        super().__init__()

    def register(self, entity, index=False):
        """Register routed entity, setting as index if ``index`` or ``entity.index`` is
        True.

        """
        entity = super().register(entity)
        if index or entity.index:
            self.redirect = entity

    def get_redirect_pattern(self, parents=None):
        """Compile the URL name to this router's redirect path, and return an
lazy RedirectView that redirects to this URL name

        """
        # this is a dirty implementation, but it works

        # we'll build the URL
        def _url_parents_ns():
            for parent in parents:
                if parent.namespace:
                    yield parent.namespace + ':'

        def _redirect():
            redirect = self.redirect
            while redirect:
                if type(redirect) is str:
                    yield self.redirect
                    break
                elif (redirect and
                      getattr(redirect, 'namespace', None) is not None):
                    yield redirect.namespace + ':'
                redirect = getattr(redirect, 'redirect', None)

        url_name = ''.join(
            chain(
                _url_parents_ns(), _redirect()
            )
        )

        url_pattern = url(
            r'^$',
            RedirectView.as_view(url=reverse_lazy(url_name))
            # TODO: Url name ?
        )

        url_pattern._redirect_url_name = url_name
        return url_pattern

    def pattern_reader(self, parents=None,
                       entity=None, add_redirect=False):
        """Read self._store and yield patterns.
        `name` can be used to filter using `entity.name`.

        """
        if parents is None:
            parents = []
        if entity is not None:
            for _entity in entity.get_pattern(parents + [self]):
                yield _entity
        else:
            if add_redirect and self.redirect is not None:
                yield self.get_redirect_pattern(parents)
            for _entity in self._store:
                # loop through store
                # if name is given, filter by entity name
                for _pattern in _entity.patterns(parents + [self]):
                    yield _pattern

    def patterns(self, parents=None, url_part=None,
                 namespace=None, entity=None,
                 add_redirect=True):
        if url_part is None:
            url_part = self.url_part

        if namespace is None:
            namespace = self.namespace

        pattern_reader = self.pattern_reader(
            parents,
            entity,
            add_redirect
        )

        # check if we need to group (by url_part and/or namespace)
        # the patterns using include
        pattern = url(
            url_part or '^',
            include(
                list(pattern_reader),
                namespace=namespace,
                app_name=namespace
            )
        )
        pattern.router = self

        yield pattern


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
