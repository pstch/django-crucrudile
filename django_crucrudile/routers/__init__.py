from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include

from django.views.generic import RedirectView


from .base import (
    BaseRoute, BaseModelRoute,
    BaseRouter, BaseModelRouter,
    provides
)

__all__ = ["Route", "ModelRoute", "Router", "ModelRouter", "provides"]


class Route(BaseRoute):
    def __init__(self, name=None, url_part=None):
        if name is not None:
            self.name = name
        elif self.name is None:
            raise Exception(
                "Route name must either be set on "
                "class or passed to __init__"
            )
        if url_part is not None:
            self.url_part = url_part
        elif self.url_part is None:
            raise Exception(
                "Route url_part must either be set on "
                "class or passed to __init__"
            )

    def patterns(self, *args, **kwargs):
        yield url("^{}$".format(self.url_part), None, name=self.name)


class ModelRoute(BaseModelRoute):
    def __init__(self, model):
        super().__init__()
        self.model = model


class Router(BaseRouter):
    """RoutedEntity that yields an URL group containing URL patterns from
    the entities in the entity store. The URL group can be set have an URL
    part, a namespace,

    """
    strict_redirect = True

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
        if label is not None:
            self.label = label
        if namespace is not None:
            self.namespace = namespace
        if url_part is not None:
            self.url_part = url_part
        if redirect is not None:
            self.redirect = redirect
        super().__init__()

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
                elif (redirect and
                      getattr(redirect, 'namespace', None) is not None):
                    url_name += redirect.namespace + ':'
                redirect = getattr(redirect, 'redirect', None)

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


class ModelRouter(BaseModelRouter, Router):
    pass
