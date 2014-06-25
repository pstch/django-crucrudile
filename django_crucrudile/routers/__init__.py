from itertools import chain

from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include

from django.db.models import Model
from django.views.generic import (
    View,
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from django.views.generic import RedirectView


from .base import (
    BaseRoute, BaseViewRoute, BaseModelRoute,
    BaseRouter, BaseModelRouter,
    provides
)

__all__ = ["Route", "ModelRoute", "Router", "ModelRouter", "provides"]


class ViewRoute(BaseViewRoute):
    """
    .. inheritance-diagram:: ViewRoute
    """
    view_class = None

    def get_callback(self):
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        return {}

class ModelRoute(BaseModelRoute, ViewRoute):
    """
    .. inheritance-diagram:: ModelRoute
    """
    def get_view_kwargs(self):
        return {'model': self.model}

    @property
    def model_url_part(self):
        return self.model._meta.model_name

    @property
    def model_url_name(self):
        return self.model._meta.model_name

    def get_url_parts(self):
        yield "^{}/{}$".format(self.model_url_part, self.url_part)

    def get_url_name(self):
        return "{}-{}".format(self.model_url_name, self.name)



class Router(BaseRouter):
    """RoutedEntity that yields an URL group containing URL patterns from
    the entities in the entity store. The URL group can be set have an URL
    part, a namespace,

    .. inheritance-diagram:: Router
    """
    @property
    def register_map(self):
        return {
            Model: ModelRouter,
            View: ViewRoute,
        }


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


class ListRoute(ModelRoute):
    name = "list"
    view_class = ListView
    index = True


class DetailRoute(ModelRoute):
    name = "detail"
    view_class = DetailView


class CreateRoute(ModelRoute):
    name = "create"
    view_class = CreateView


class UpdateRoute(ModelRoute):
    name = "update"
    view_class = UpdateView


class DeleteRoute(ModelRoute):
    name = "delete"
    view_class = DeleteView


@provides(ListRoute)
@provides(DetailRoute)
@provides(CreateRoute)
@provides(UpdateRoute)
@provides(DeleteRoute)
class ModelRouter(BaseModelRouter, Router):
    """
    .. inheritance-diagram:: ModelRouter
    """
    pass
