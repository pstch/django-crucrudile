from functools import partial
from itertools import chain

from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy

from django.db.models import Model
from django.views.generic import (
    View, RedirectView,
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django_crucrudile.routes import ViewRoute, ModelViewRoute
from django_crucrudile.entity import Entity
from django_crucrudile.entity.store import EntityStore, provides

__all__ = ["Router", "ModelRouter", "provides"]


class Router(EntityStore, Entity):
    """RoutedEntity that yields an URL group containing URL patterns from
    the entities in the entity store. The URL group can be set have an URL
    part and a namespace.

    .. inheritance-diagram:: Router
    """
    namespace = None
    """
    :attribute namespace: If defined, group this router's patterns in
                          an URL namespace
    :type namespace: str
    """
    url_part = None
    """
    :attribute url_part: If defined, add to router URL (use when as
                         regex when building URL group)
    :type url_part: str
    """
    redirect = None
    """
    :attribute redirect: If defined, Router will add a redirect view
                         to the returned patterns. To get the redirect
                         target, ``get_redirect_pattern()`` will
                         follow ``redirect`` attributes in the stored
                         entities.
    :type redirect: Router:
    """
    def __init__(self, *args,
                 label=None, namespace=None,
                 url_part=None, redirect=None,
                 **kwargs):
        """Initialize Router base attributes

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
        super().__init__(*args, **kwargs)

    def get_register_map(self):
        """Basic register map, passes models to a ModelRouter, Django views to
        a ViewRoute.

        """
        mapping = super().get_register_map()
        mapping.update({
            Model: ModelRouter,
            View: ViewRoute,
        })
        return mapping

    def register(self, entity, index=False):
        """Register routed entity

        Override to allow setting as index when
        ``index`` or ``entity.index`` is True.

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
        """Read self._store and yield a pattern of an URL group (with url part
        and namespace) containing entities's patterns (obtained using
        ``pattern_reader``), also yield redirect patterns where defined.

        """
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


class BaseModelRouter(Router):
    """ModelRouter with no views. Give ``model`` kwarg where needed, ask
    it in ``__init__``, and map SingleObjectMixin and
    MultipleObjectMixin to ModelViewRoute in register functions.

    .. inheritance-diagram:: BaseModelRouter

    """
    model = None
    """
    :attribute model: Model used when building router URL name and URL
                      part, and passed to registered routes.
    :type model: model
    """
    def register_map_kwargs(self):
        """Give model as kwarg when applying register_map. """
        kwargs = super().get_register_map_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def get_base_store_kwargs(self):
        """Add ModelRouter model to upstream auto register kwargs, so that the
        route classes in the base store will get the model as a kwarg when
        being instantiated.

        """
        kwargs = super().get_base_store_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def __init__(self, *args, model=None, **kwargs):
        """Check for model in kwargs, if None and not defined at class-level,
        fail.

        :raises ValueError: if model not passed an argument and not
                            defined on class

        """
        # we need to set self.model before calling the superclass
        # __init__, because it will call
        # self.get_auto_register_kwargs() which needs self.model
        if model is not None:
            self.model = model
        elif self.model is None:
            raise ValueError(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(*args, **kwargs)

    def get_register_map(self):
        """Override to append mapping of SingleObjectMixin and
MultipleObjectMixin to ModelViewRoute.

        """
        mapping = super().get_register_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute,
            View: ViewRoute,
        })
        return mapping

    @classmethod
    def get_register_class_map(cls):
        """Override to append mapping of ``SingleObjectMixin`` and
        ``MultipleObjectMixin`` to ``ModelViewRoute.make_for_view`` .

        We use ``make_for_view`` because we are here registering the
        class map (base store), whose values are themselves classes
        (Entity classes), that will be called the get the registered
        entity instance.

        ``make_for_view`` creates a new ModelViewRoute class, and uses
        its argument as the ``view_class`` class attribute.

        (if we returned directly ``ModelViewRoute`` in the mapping,
        the registered entity **class** would be an entity
        **instance**).

        """
        mapping = super().get_register_class_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute.make_for_view
        })
        return mapping


@provides(ListView, index=True)
@provides(DetailView)
@provides(CreateView)
@provides(UpdateView)
@provides(DeleteView)
class ModelRouter(BaseModelRouter):
    """Routes Django generic views with the model given in instantiation.

    .. inheritance-diagram:: ModelRouter
    """
