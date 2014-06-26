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

__all__ = [
    "Router", "BaseModelRouter",
    "ModelRouter"
]


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
    :attribute redirect: If defined, :class:`Router` will add a redirect view
                         to the returned patterns. To get the redirect
                         target, :func:`get_redirect_pattern` will
                         follow ``redirect`` attributes in the stored
                         entities.
    :type redirect: :class:`django_crucrudile.entity.Entity`
    """
    def __init__(self,
                 namespace=None,
                 url_part=None,
                 redirect=None,
                 **kwargs):
        """Initialize Router base attributes

        :argument namespace: see :attr:`url_part`
        :argument url_part: see :attr:`redirect`
        :argument redirect: see :attr:`redirect`
        """
        # initialize base attributes
        if namespace is not None:
            self.namespace = namespace
        if url_part is not None:
            self.url_part = url_part
        if redirect is not None:
            self.redirect = redirect

        # call superclass implementation of __init__
        super().__init__(**kwargs)

    def get_register_map(self):
        """Basic register map, passes models to a
        :class:`django_crucrudile.routers.ModelRouter`, Django views
        to a :class:`django_crucrudile.routes.ViewRoute`

        """
        mapping = super().get_register_map()
        mapping.update({
            Model: ModelRouter,
            View: ViewRoute,
        })
        return mapping

    def register(self, entity, index=False):
        """Register routed entity

        Set as index when ``entity``
        or :attr:`django_crucrudile.entity.Entity.index`` is True.

        :argument entity: Entity to register
        :type entity: :class:`django_crucrudile.entity.Entity`
        :argument index: Register as index
        :type index: bool
        """
        entity = super().register(entity)
        if index or entity.index:
            self.redirect = entity

    def get_redirect_pattern(self, parents=None):
        """Compile the URL name to this router's redirect path, and return a
lazy ``RedirectView`` that redirects to this URL name

        :argument parents: The list of parent routers will be used to
                           get the current namespaces when building
                           the redirect URL name
        :type parents: list of :class:`django_crucrudile.routers.Router`
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

    def patterns(self, parents=None, add_redirect=True):
        """Read :attr:`_store` and yield a pattern of an URL group (with url part
        and namespace) containing entities's patterns (obtained from
        the entity store), also yield redirect patterns where defined.

        :argument parents: We need :func:`patterns` to pass
                           ``parents`` recursively, because it
                           may be needed to make redirect URL patterns
        :type parents: list of :class:`django_crucrudile.routers.Router`
        :argument add_redirect: Add a redirect pattern if there is one
                                defined
        :type add_redirect: bool
        """
        # get url_part and namespace (needed when building
        # RegexURLResolver)
        url_part = self.url_part
        namespace = self.namespace

        # initialize default arguments
        if parents is None:
            parents = []

        # yield redirect pattern if there is one defined (and
        # add_redirect is True)
        if add_redirect and self.redirect is not None:
            yield self.get_redirect_pattern(parents)

        # define a pattern reader generator, yielding patterns from the
        # store entities
        def _pattern_reader():
            for entity in self._store:
                for pattern in entity.patterns(
                    parents + [self], add_redirect
                ):
                    yield pattern

        # consume the generator
        pattern_list = list(_pattern_reader())

        # make a RegexURLResolver
        pattern = url(
            url_part or '^',
            include(
                pattern_list,
                namespace=namespace,
                app_name=namespace
            )
        )
        pattern.router = self

        yield pattern


class BaseModelRouter(Router):
    """ModelRouter with no views. Give :attr:`model` kwarg where needed,
    ask it in :func:`__init__`, and map ``SingleObjectMixin`` and
    ``MultipleObjectMixin`` to
    :class:`django_crucrudile.routes.ModelViewRoute` in register
    functions.

    .. inheritance-diagram:: BaseModelRouter

    """
    model = None
    """
    :attribute model: Model used when building router URL name and URL
                      part, and passed to registered routes. Must be
                      defined at class-level or passed to
                      :func:`__init__`.
    :type model: model
    """
    def register_map_kwargs(self):
        """Give :attr:`model` as kwarg when applying register map. """
        kwargs = super().get_register_map_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def get_base_store_kwargs(self):
        """Add :attr:`model` to upstream auto register kwargs, so that the
        route classes in the base store will get the model as a kwarg when
        being instantiated.

        """
        kwargs = super().get_base_store_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def __init__(self, model=None, **kwargs):
        """Check for :argument:`model` in kwargs, if None and not defined at
        class-level, fail.

        :argument model: see :attr:`model`
        :type model: :class:`django.db.Models`

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
        super().__init__(**kwargs)

    def get_register_map(self):
        """Override to append mapping of ``SingleObjectMixin`` and
        ``MultipleObjectMixin`` to
        :class:`django_crucrudile.routes.ModelViewRoute`.

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
        ``MultipleObjectMixin`` to
        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        .

        We use
        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        because we are here registering the class map (base store),
        whose values are themselves classes (Entity classes), that
        will be called the get the registered entity instance.

        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        creates a new :class:`django_crucrudile.routes.ModelViewRoute`
        class, and uses its argument as the
        :attr:`django_crucrudile.routes.ViewRoute.view_class` class
        attribute.

        (if we returned directly a
        :class:`django_crucrudile.routes.ModelViewRoute` in the
        mapping, the registered entity "class" would be an entity
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
