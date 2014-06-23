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

    @property
    def url_part(self):
        pass


class ModelRoute(BaseModelRoute):
    pass


class Router(BaseRouter):
    register_transform_map = None
    strict_redirect = True
    auto_label = False
    auto_namespace = False

    def __init__(self, name=None, label=None, namespace=None):
        if label is None and self.auto_label:
            # todo: translate name
            label = name
        if namespace is None and self.auto_namespace:
            # todo: translate name
            namespace = name

        super().__init__(name, label, namespace)
        self._store = []

    @property
    def url_part(self):
        return self.namespace

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
        if index:
            self.redirect = entity

    def get_redirect_url_name(self, parents=None, strict=None):
        if parents is None:
            parents = []

        if strict is None:
            strict = self.strict_redirect

        if type(self.redirect) is str:
            return super().get_redirect_url_name(parents, strict)

        elif self.redirect is not None:
            name = self.redirect.get_redirect_url_name(
                parents + [self], strict
            )
            if name is not None:
                return name
            else:
                raise NoRedirectReturnedException(
                    "Redirect URL resolution failed. Current path '{}', "
                    "registered redirect ({} on {}) did not return an URL "
                    "name".format(
                        ' > '.join(str(parent) for parent in parents + [self]),
                        self.redirect,
                        self
                    )
                )
        elif strict:
                raise NoRedirectDefinedException(
                    "Redirect URL resolution failed. Current path '{}', "
                    "no redirect is registered on {}".format(
                        ' > '.join(str(parent) for parent in parents + [self]),
                        self
                    )
                )

    def get_redirect_pattern(self, parents=None):
        if self.redirect:
            if type(self.redirect) is str:
                url_name = self.redirect
            else:
                url_name = self.get_redirect_url_name(parents)
            return url(
                r'^$',
                RedirectView.as_view(url=reverse_lazy(url_name))
                # TODO: Url name ?
            )
        else:
            raise NoRedirectDefinedException(
                "Cannot get redirect pattern, `redirect` attribute is None."
            )

    def pattern_reader(self, parents=None, name=None,
                       entity=None, add_redirect=False):
        """Read self._store and yield patterns.
        `name` can be used to filter using `entity.name`.

        """
        if parents is None:
            parents = []
        if entity is not None:
            for pattern in entity.patterns(parents + [self]):
                yield pattern
        else:
            if add_redirect and name is None and self.redirect is not None:
                yield self.get_redirect_pattern(parents)
            for _entity in self._store:
                # loop through store
                if name is None or _entity.name == name:
                    # if name is given, filter by entity name
                    for pattern in _entity.patterns(parents + [self]):
                        yield pattern

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
        if url_part is not None or namespace is not None:
            yield url(
                r'^{}$'.format(url_part or ''),
                include(
                    list(pattern_reader),
                    namespace=namespace,
                    app_name=namespace
                )
            )
        else:
            # no need to group, yield patterns
            for pattern in pattern_reader:
                yield pattern


class ModelRouter(BaseModelRouter):
    pass
