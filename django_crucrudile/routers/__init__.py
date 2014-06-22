from collections import defaultdict
from abc import ABCMeta, abstractmethod, abstractproperty

from django.core.urlresolvers import reverse
from django.utils.functional import lazy


class RoutedEntity(metaclass=ABCMeta):
    @abstractmethod
    def patterns(self, parents=None, url_part=None, namespace=None, name=None, entity=None, add_redirect=True):
        pass

    @abstractmethod
    def get_redirect_url_name(self, parents=None, strict=None):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def url_part(self):
        pass

class BaseRoute(RoutedEntity):
    pass

class BaseModelRoute(BaseRoute):
    pass

class Route(BaseRoute):
    ### HERE ###
    pass

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
        self._store = []

        self.redirect = redirect
        self.label = label
        self.namespace = namespace

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
                if (base is None or \
                    isinstance(entity, base) or \
                    (isinstance(entity, type) and \
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
        else:
            parents = list(parents)

        if strict is None:
            strict = self.strict_redirect

        parents.append(self)

        if type(self.redirect) is str:
            def _url_full_name():
                for parent in parents:
                    if parent.namespace is not None:
                        yield parent.namespace
                yield self.redirect

            return ":".join(_url_full_name())

        elif self.redirect is not None:
            name = self.redirect.get_redirect_url_name(parents, strict)
            if name is not None:
                return name
            else:
                raise Exception(
                    "Redirect URL resolution failed. Current path '{}', "
                    "registered redirect ({} on {}) did not return an URL "
                    "name".format(
                        ' > '.join(str(parent) for parent in parents),
                        self.redirect,
                        self
                    )
                )
        elif strict:
                raise Exception(
                    "Redirect URL resolution failed. Current path '{}', "
                    "no redirect is registered on {}".format(
                        ' > '.join(str(parent) for parent in parents),
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
            raise Exception("Cannot get redirect pattern, `redirect` attribute is None.")

    def pattern_reader(self, parents=None, name=None, entity=None, add_redirect=False):
        """Read self._store and yield patterns.
        `name` can be used to filter using `entity.name`.

        """
        if parents is None:
            parents = []
        else:
            parents = list(parents)

        parents.append(self)

        if entity is not None:
            for pattern in entity.patterns(parents):
                yield pattern
        else:
            if add_redirect and name is None and self.redirect is not None:
                yield self.get_redirect_pattern(parents, self.redirect)
            for _entity in self._store:
                # loop through store
                if name is None or _entity.name == name:
                    # if name is given, filter by entity name
                    for pattern in _entity.patterns(parents):
                        yield pattern

    def patterns(self, parents=None, url_part=None, namespace=None, name=None, entity=None, add_redirect=True):
        if url_part is None:
            url_part = self.url_part

        if namespace is None:
            namespace = self.namespace

        # check if we need to group (by url_part and/or namespace)
        # the patterns using include
        if self.url_part is not None or self.namespace is not None:
            yield url(
                r'^{}$'.format(url_part or ''),
                include(
                    self.pattern_reader(parents, name, entity, add_redirect),
                    namespace=namespace,
                    app_name=namespace
                )
            )
        else:
            # no need to group, yield patterns
            for pattern in pattern_reader(parents, name, entity, add_redirect):
                yield pattern


class ModelRouter(BaseModelRouter):
    pass
