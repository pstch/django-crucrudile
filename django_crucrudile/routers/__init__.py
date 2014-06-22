from abc import ABCMeta, abstractmethod, abstractproperty

from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include

from django.views.generic import RedirectView


from django_crucrudile.exceptions import (
    NoRedirectDefinedException, NoRedirectReturnedException
)


class RoutedEntity(metaclass=ABCMeta):
    url_next_sep = ':'
    namespace = None

    def __init__(self, label=None, namespace=None, redirect=None):
        self.label = label
        self.namespace = namespace
        self.redirect = redirect

    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        pass

    def get_redirect_url_name(self, parents=None, strict=None):
        if self.redirect:
            def _url_full_name():
                for parent in parents + [self]:
                    if parent.namespace is not None:
                        yield parent.namespace
                        yield parent.url_next_sep
                yield self.redirect

            return ''.join(_url_full_name())
        else:
            raise NoRedirectDefinedException(
                "Redirect URL resolution failed. Current path '{}', "
                "no redirect is registered on {}".format(
                    ' > '.join(str(parent) for parent in parents + [self]),
                    self
                )
            )

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def url_part(self):
        pass

    @property
    def redirect(self):
        return self._redirect

    @redirect.setter
    def redirect(self, value):
        self._redirect = value


class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class Route(BaseRoute):
    def patterns(self, *args, **kwargs):
        print(
            "patterns() called on Route {} {}".format(args, kwargs)
        )
        yield

    def get2_redirect_url_name(self, *args, **kwargs):
        print(
            "get_redirect_url_name() called on Route "
            "{} {}".format(args, kwargs)
        )

    @property
    def name(self):
        print(
            "name getter called on Route"
        )

    @property
    def url_part(self):
        print(
            "url_part getter called on Route"
        )

class ModelRoute(BaseModelRoute):
    pass


class BaseRouter(RoutedEntity):
    pass


class BaseModelRouter(BaseRouter):
    pass


class Router(BaseRouter):
    register_transform_map = None
    strict_redirect = True

    def __init__(self, label=None, namespace=None, redirect=None):
        super().__init__(label, namespace, redirect)
        self._store = []

    @property
    def name(self):
        return self.namespace

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
        if self.url_part is not None or self.namespace is not None:
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
