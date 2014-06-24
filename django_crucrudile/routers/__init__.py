from abc import ABCMeta

from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include

from django.views.generic import RedirectView

from django_crucrudile.exceptions import (
    NoRedirectDefinedException, NoRedirectReturnedException
)

from .base import (
    BaseRoute, BaseModelRoute,
    BaseRouter, BaseModelRouter,
)


class Route(BaseRoute):
    def patterns(self, *args, **kwargs):
        yield


class ModelRoute(BaseModelRoute):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.name = "{}-{}".format(self.model, self.name)


class RouterMetaclass(ABCMeta):
    _base_store = []

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._base_store = list(cls._base_store)


def provides(provided):
    def patch_router(router):
        router.register_class(provided)
        return router
    return patch_router


class Router(BaseRouter, metaclass=RouterMetaclass):
    _base_store = []
    register_transform_map = None
    strict_redirect = True
    auto_label = False
    auto_namespace = False
    auto_url_part = True

    @classmethod
    def register_class(self, cls):
        """Add a route class to _base_store. This route class will be
        instantiated (with kwargs from get_auto_register_kwargs())
        when the Router is itself instiated, using
        register_base_store()

        """
        self._base_store.append(cls)

    def __init__(self, name=None, label=None,
                 namespace=None, url_part=None):
        """Initialize Router base attributes, initialize entity store _store,
        and instantiate entities from entity classes in _base_store

        """
        if (
                label is None and
                name is not None and
                self.auto_label
        ):
            # todo: translate name
            label = name
        if (
                namespace is None and
                name is not None and
                self.auto_namespace
        ):
            # todo: translate name
            namespace = name
        if (
                url_part is None and
                name is not None and
                self.auto_url_part
        ):
            url_part = name

        super().__init__(name, label, namespace, url_part)
        self._store = []
        self.register_base_store()

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
        if self.register_transform_map:
            transform_kwargs = transform_kwargs or {}
            for base, func in self.register_transform:
                if (base is None or
                    isinstance(entity, base) or
                    (isinstance(entity, type) and
                     issubclass(entity, base))):
                    return func(entity, **transform_kwargs)
            else:
                raise TypeError(
                    "A register transform mapping is defined, but could "
                    "not find a correspondant mapping for {}".format(entity)
                )
        else:
            return entity

    def register(self, entity, index=False):
        self._store.append(entity)
        if index or entity.index:
            self.redirect = entity

    def get_redirect_pattern(self, parents=None):
        if self.redirect:
            url_name = ""
            for parent in parents:
                if parent.namespace:
                    url_name += parent.namespace + ':'
            redirect = self.redirect
            while redirect:
                if type(redirect) is str:
                    url_name += str(self.redirect) + "HAA"
                    break
                elif redirect and redirect.namespace is not None:
                    url_name += redirect.namespace + ':'
                redirect = getattr(redirect, 'redirect', None)

            url_pattern = url(
                r'^$',
                RedirectView.as_view(url=reverse_lazy(url_name))
                # TODO: Url name ?
            )
            url_pattern._redirect_url_name = url_name
            return url_pattern

    def pattern_reader(self, parents=None, name=None,
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
            if add_redirect and name is None and self.redirect is not None:
                yield self.get_redirect_pattern(parents)
            for _entity in self._store:
                # loop through store
                if name is None or _entity.name == name:
                    # if name is given, filter by entity name
                    for _pattern in _entity.patterns(parents + [self]):
                        yield _pattern

    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        if url_part is None:
            url_part = self.url_part

        if namespace is None:
            namespace = self.namespace

        pattern_reader = self.pattern_reader(
            parents,
            name,
            entity,
            add_redirect
        )

        # check if we need to group (by url_part and/or namespace)
        # the patterns using include
        ret = url(
            url_part or '^',
            include(
                list(pattern_reader),
                namespace=namespace,
                app_name=namespace
            )
        )
        ret.router = self

        yield ret


class ModelRouter(Router):
    def __init__(self, *args, **kwargs):
        model = kwargs['model']
        self.model = model
        super().__init__(args, kwargs)
        self.name = model

    def get_auto_register_kwargs(self):
        kwargs = super().get_auto_register_kwargs()
        kwargs['model'] = self.model
        return kwargs
