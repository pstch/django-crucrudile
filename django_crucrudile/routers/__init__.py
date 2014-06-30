"""A router is an implementation of the abstract class Entity, that
uses an entity store to allow routing other entities. In the code,
this is represented by subclassing
:class:`django_crucrudile.entities.store.EntityStore` and
:class:`django_crucrudile.entities.Entity`, and providing a generator in
``patterns()``, yielding URL patterns made from the entity
store. Providing :func:`django_crucrudile.entities.Entity.patterns`
makes router classes concrete implementations of the Entity abstract
class, which allows them to be used in entity stores.

This module contains three implementations of routers, a simple one,
and two implementations adapted to Django models :

 - :class:`Router` : implements the abstract class
   :class:`django_crucrudile.entities.Entity`, and subclassing
   :class:`django_crucrudile.entities.store.EntityStore` to implement
   :func:`Router.patterns`
 - :class:`BaseModelRouter` : subclasses :class:`Router`,
   instantiate with a model as argument, adapted to pass that
   model as argument to registered entity classes
 - :class:`ModelRouter` : that subclasses :class:`BaseModelRouter`
   along with a set of default
   :class:`django_crucrudile.routes.ModelViewRoute` for the five
   default Django generic views.

"""
from uuid import uuid4

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
from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore, provides

__all__ = [
    "Router", "BaseModelRouter",
    "ModelRouter"
]


def _random_url_id():
    return uuid4().hex[:6]

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
    :type redirect: :class:`django_crucrudile.entities.Entity`
    """
    add_redirect = None
    """
    :attribute add_redirect: Add redirect pattern when calling
                             :func:`patterns`. If None, will be
                             guessed using :attribute:`redirect`
    :type add_redirect: bool or None
    """
    add_redirect_silent = False
    """
    :attribute add_redirect_silent: Fail silently when the patterns
                                    reader is asked to add the
                                    redirect patterns and the redirect
                                    attribute is not set (on
                                    self). Defaults to False, because
                                    in the default configuration,
                                    :attribute:`add_redirect` is
                                    guessed using
                                    :attribute:`redirect`, using
                                    ``bool``. Set to True if you're
                                    using :attribute:`add_redirect`
                                    explicitly and want the redirect
                                    attribute to be optional.
    :type add_redirect_silent: bool
    """
    get_redirect_silent = False
    """
    :attribute get_redirect_silent: Fail silently when following
                                    redirect attributes to find the
                                    redirect URL name (if no URL name
                                    is found).
    :type get_redirect_silent: bool
    """

    def __init__(self,
                 namespace=None,
                 url_part=None,
                 redirect=None,
                 add_redirect=None,
                 add_redirect_silent=None,
                 get_redirect_silent=None,
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
        if add_redirect is not None:
            self.add_redirect = add_redirect
        if add_redirect_silent is not None:
            self.add_redirect_silent = add_redirect_silent
        if get_redirect_silent is not None:
            self.get_redirect_silent = get_redirect_silent

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
        or :attr:`django_crucrudile.entities.Entity.index`` is True.

        :argument entity: Entity to register
        :type entity: :class:`django_crucrudile.entities.Entity`
        :argument index: Register as index
        :type index: bool
        """
        entity = super().register(entity)
        if index or entity.index:
            self.redirect = entity

    def get_redirect_pattern(self, namespaces=None, silent=None):
        """Compile the URL name to this router's redirect path (found by
        following :attribute:`Router.redirect`), and that return a lazy
        ``RedirectView`` that redirects to this URL name

        :argument namespaces: The list of namespaces will be used to
                              get the current namespaces when building
                              the redirect URL name
        :type namespaces: list of str
        :argument silent: Override
                          :attribute:`Router.get_redirect_silent`
        :type silent: bool

        :raise ValueError: If no redirect found when following
                           ``redirect`` attributes, and silent
                           mode is not enabled.

        """
        # initialize default arguments
        if silent is None:
            silent = self.get_redirect_silent
        if namespaces is None:
            namespaces = []
        else:
            # need to copy because _follow_redirect appends namespaces
            # found when following redirect attributes
            namespaces = list(namespaces)

        # used if following redirect attributes failed, to provide
        # information in the exception.
        _last_redirect_found = None

        # maybe a while loop is better here, especially for handling
        # _last_redirect_found. I can't decide.
        def _follow_redirect(redirect):
            # loop through redirect attributes
            nonlocal _last_redirect_found
            if isinstance(redirect, str):
                # if it's a string, no need to follow any more (we
                # have the URL name to redirect to and all namespaces in
                # parent redirects have been added)
                return redirect
            elif redirect is not None:
                # not a string and not None, check if it's a Router so
                # we can get a namespace check that subclass of Router
                # because it's in Router that the namespace attribute is
                # defined.

                # maybe it's better to just getattr(redirect,
                # 'namespace') and to handle the exception (or
                # getattr(redirect, 'namespace', None)).

                # can't decide either
                if issubclass(redirect, Router) and redirect.namespace:
                    namespaces.append(redirect.namespace)
                # save last redirect in case of exception
                _last_redirect_found = redirect
                # NOTE: risk of recursive loop here, if the redirect
                # attributes keeps being not None and never string
                # this could happen if case of "redirect loop" :
                # >>> A, B = [Router() for _ in range(3)]
                # >>> A.redirect = B
                # >>> B.redirect = A
                # >>> _follow_redirect(A)
                # --- /!\ infinite loop /!\ ---
                return _follow_redirect(redirect.redirect)

        # here, "raw" means "not prefixed with namespaces"
        raw_target_url_name = _follow_redirect(self.redirect)

        if raw_target_url_name:
            # get the target URL name (by prefixing the raw version
            # with the namespaces)
            target_url_name = ':'.join([
                ':'.join(namespaces),
                raw_target_url_name
            ]) if namespaces else raw_target_url_name

            # Create an identifier for the redirection pattern.
            # This is not required as these patterns should not be
            # pointed to directly, but it helps when debugging
            # (use a random ID to avoid collisions)
            redirect_url_name = "{}-redirect".format(
                raw_target_url_name,
            )

            # Create a redirect view, that will get the URL to
            # redirect to lazily (when it's accessed), as the target
            # URL is not known yet
            redirect_view = RedirectView.as_view(
                url=reverse_lazy(target_url_name)
            )

            # Now that we have a redirect view pointing to the target
            # pattern, and a name for our pattern, we can create it
            url_pattern = url(
                r'^$',
                redirect_view,
                name=redirect_url_name
            )

            # FIXME: Used for debugging, should be removed.
            url_pattern._redirect_url_name = target_url_name

            return url_pattern
        elif not silent:
            # No URL found and set to fail (not silent) if we got
            # here, it's because _follow_redirect() returned
            # None.
            #
            # This will happen if self.redirect is None or if
            # following redirect attributes returned None somewhere
            raise ValueError(
                "Failed following redirect attribute {} "
                "(last redirect found : {}) in {}"
                "".format(
                    self.redirect,
                    _last_redirect_found,
                    self
                )
            )

    def patterns(self, namespaces=None,
                 add_redirect=None, add_redirect_silent=None):
        """Read :attr:`_store` and yield a pattern of an URL group (with url part
        and namespace) containing entities's patterns (obtained from
        the entity store), also yield redirect patterns where defined.

        :argument namespaces: We need :func:`patterns` to pass
                              ``namespaces`` recursively, because it
                              may be needed to make redirect URL patterns
        :type namespaces: list of str
        :argument add_redirect: Override :attribute:`Router.add_redirect`
        :type add_redirect: bool
        :argument add_redirect_silent: Override
                                       :attribute:`Router.add_redirect_silent`
        :type add_redirect: bool
        """
        # initialize default arguments

        # append self.namespace (if any) to given namespaces (copying
        # the given namespace list because we will be altering it)
        if namespaces is None:
            namespaces = [self.namespace] if self.namespace else []
        elif self.namespace:
            namespaces = namespaces + [self.namespace]

        # (we copy some attributes to other variables so that we can
        # pass their original values recursively)
        orig_add_redirect = add_redirect
        orig_add_redirect_silent = add_redirect_silent

        # If add_redirect not given, get from attributes ; If None
        # found, guess from boolean value of self.redirect
        if add_redirect is None:
            if self.add_redirect is not None:
                add_redirect = self.add_redirect
            else:
                add_redirect = bool(self.redirect)
        else:
            add_redirect = add_redirect
        # if add_redirect_silent not given, get from attributes
        if add_redirect_silent is None:
            add_redirect_silent = self.add_redirect_silent

        # get url_part and namespace from attributes
        # (needed when building RegexURLResolver)
        url_part = self.url_part
        namespace = self.namespace

        # get redirect (needed if add_redirect is True)
        redirect = self.redirect

        # define a pattern reader generator, yielding patterns from the
        # store entities (also get the redirect pattern if required)
        def pattern_reader():
            # yield redirect pattern if there is one defined (and
            # add_redirect is True)
            if add_redirect:
                if redirect is not None:
                    redirect_pattern = self.get_redirect_pattern(namespaces)
                    if redirect_pattern:
                        yield redirect_pattern
                else:
                    if add_redirect_silent is False:
                        raise ValueError(
                            "No redirect attribute set on {} "
                            "(and `add_redirect_silent` is True)."
                            "".format(self)
                        )

            for entity in self._store:
                # yield patterns from each entity's patterns function
                for pattern in entity.patterns(
                        namespaces,
                        orig_add_redirect,
                        orig_add_redirect_silent
                ):
                    yield pattern

        # consume the generator
        pattern_list = list(pattern_reader())

        # make a RegexURLResolver
        pattern = url(
            '^{}/'.format(url_part) if url_part else '^',
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
    def get_register_map_kwargs(self):
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

    def __init__(self, model=None, url_part=None, **kwargs):
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
        if url_part is not None:
            self.url_part = url_part
        else:
            self.url_part = self.model_url_part
        super().__init__(**kwargs)

    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part"""
        return self.model._meta.model_name

    def get_register_map(self):
        """Override to append mapping of ``SingleObjectMixin`` and
        ``MultipleObjectMixin`` to
        :class:`django_crucrudile.routes.ModelViewRoute`.

        """
        mapping = super().get_register_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute,
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

    Provides specific ModelViewRoute classes, created for the
    following Django generic views :

     - :class:`django.views.generic.ListView`
     - :class:`django.views.generic.DetailView`
     - :class:`django.views.generic.CreateView`
     - :class:`django.views.generic.UpdateView`
     - :class:`django.views.generic.DeleteView`

    These classes are registered in the base store, using
    :func:`django_crucrudile.entities.store.EntityStore.register_class`
    or the :func:`django_crucrudile.entities.store.provides`
    decorator. They will be instantiated (with the model as argument,
    obtained from :func:`BaseModelRouter.__init__`) when the router is
    itself instantiated, using
    :func:`django_crucrudile.entities.store.EntityStore.register_base_store`.

    """
