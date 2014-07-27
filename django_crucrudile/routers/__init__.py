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
 - :class:`model.ModelRouter` : subclasses :class:`Router`,
   instantiate with a model as argument, adapted to pass that
   model as argument to registered entity classes
 - :class:`model.generic.GenericModelRouter` : that subclasses
   :class:`model.ModelRouter` along with a set of default
   :class:`django_crucrudile.routes.ModelViewRoute` for the five
   default Django generic views.

"""
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy

from django.db.models import Model
from django.views.generic import (
    View, RedirectView,
)

from django_crucrudile.routes import ViewRoute
from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore

__all__ = [
    "Router",
    "ModelRouter",
    "GenericModelRouter"
]


class Router(EntityStore, Entity):
    """RoutedEntity that yields an URL group containing URL patterns from
    the entities in the entity store
    (:class:`django_crucrudile.entities.store.EntityStore`). The URL
    group can be set have an URL part and na namespace.

    Also handles URL redirections : allows setting an Entity as
    "index", which means that it will become the default routed entity
    for the parent entity (implementation details in
    :func:`get_redirect_pattern`).

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
    :attribute redirect: If defined, :class:`Router` will add a
                         redirect view to the returned patterns. To
                         get the redirect target,
                         :func:`get_redirect_pattern` will follow
                         ``redirect`` attributes in the stored
                         entities. The attribute's value is altered by
                         the :func:`register`, if ``index`` is
                         ``True`` in its arguments or if the
                         registered entity
                         :attr:`django_crucrudile.entities.Entity.index`
                         attribute is set to True.
    :type redirect: :class:`django_crucrudile.entities.Entity`
    """
    add_redirect = None
    """
    :attribute add_redirect: Add redirect pattern when calling
                             :func:`patterns`. If None (default), will
                             be guessed using :attr:`redirect` (Add
                             redirect only if there is one defined)
    :type add_redirect: bool
    """
    add_redirect_silent = False
    """
    :attribute add_redirect_silent: Fail silently when the patterns
                                    reader is asked to add the
                                    redirect patterns and the redirect
                                    attribute is not set (on
                                    self). Defaults to False, because
                                    in the default configuration,
                                    :attr:`add_redirect` is
                                    guessed using
                                    :attr:`redirect`, using
                                    ``bool``. Set to True if you're
                                    using :attr:`add_redirect`
                                    explicitly and want the redirect
                                    pattern to be optional.
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
    redirect_max_depth = 100
    """
    :attribute redirect_max_depth: Max depth when following redirect
                                   attributes
    :type redirect_max_depth: int
    """
    generic = False
    """
    :attribute generic: If True, :func:`get_register_map` will return
                        a :class:`model.generic.GenericModelRouter`
                        (with preconfigured Django videws) for the
                        ``Model`` type.
    :type generic: bool
    """
    def __init__(self,
                 namespace=None,
                 url_part=None,
                 redirect=None,
                 add_redirect=None,
                 add_redirect_silent=None,
                 get_redirect_silent=None,
                 generic=None,
                 **kwargs):  # pragma: no cover
        """Initialize Router base attributes from given arguments

        :argument namespace: Optional. See :attr:`namespace`
        :argument url_part: Optional. See :attr:`url_part`
        :argument redirect: Optional. See :attr:`redirect`
        :argument add_redirect: Optional. See :attr:`add_redirect`
        :argument add_redirect_silent: Optional. See
                                       :attr:`add_redirect_silent`
        :argument get_redirect_silent: Optional. See
                                       :attr:`get_redirect_silent`
        :argument generic: Optional. See :attr:`generic`

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
        if generic is not None:
            self.generic = generic

        # call superclass implementation of __init__
        super().__init__(**kwargs)

    def get_register_map(self):
        """Add two base register mappings (to the mappings returned by the
super implementation)

        - :class:`django.db.models.Model` subclasses are passed to a
          :class:`model.ModelRouter` (or
          :class:`model.generic.GenericModelRouter`) if
          :attr:`generic` is set to ``True``)
        - :class:`django.views.generic.View` subclasses are passed to a View

        :returns: Register mappings
        :rtype: dict

        """
        mapping = super().get_register_map()
        mapping.update({
            Model: ModelRouter if not self.generic else GenericModelRouter,
            View: ViewRoute,
        })
        return mapping

    def register(self, entity, index=False, map_kwargs=None):
        """Register routed entity, using
        :func:`django_crucrudile.entities.store.EntityStore.register`

        Set as index when ``index`` or ``entity.index`` is True.

        :argument entity: Entity to register
        :type entity: :class:`django_crucrudile.entities.Entity`
        :argument index: Register as index (set :attr:`redirect` to ``entity``
        :type index: bool
        :argument map_kwargs: Optional. Keyword arguments to pass to
                              mapping value if entity gets
                              transformed.
        :type map_kwargs: dict

        >>> from mock import Mock
        >>> router = Router()

        >>> entity = Mock()
        >>> entity.index = False
        >>>
        >>> router.register(entity)
        >>> router.redirect is None
        True

        >>> entity = Mock()
        >>> entity.index = False
        >>>
        >>> router.register(entity, index=True)
        >>> router.redirect is entity
        True

        >>> entity = Mock()
        >>> entity.index = True
        >>>
        >>> router.register(entity)
        >>> router.redirect is entity
        True

        """
        entity = super().register(
            entity,
            map_kwargs=map_kwargs
        )
        if index or entity.index:
            self.redirect = entity

    def get_redirect_pattern(self, namespaces=None, silent=None,
                             redirect_max_depth=None):
        """Compile the URL name to this router's redirect path (found by
        following :attr:`Router.redirect`), and that return a lazy
        :class:`django.views.generic.RedirectView` that redirects to
        this URL name

        :argument namespaces: Optional. The list of namespaces will be
                              used to get the current namespaces when
                              building the redirect URL name. If not
                              given an empty list will be used.
        :type namespaces: list of str
        :argument silent: Optional. See
                          :attr:`Router.get_redirect_silent`
        :type silent: bool
        :argument redirect_max_depth: Optional. See
                                         :attr:`Router.redirect_max_depth`
        :type redirect_max_depth: int

        :raise OverflowError: If the depth-first search in the graph
                              made from redirect attributes reaches
                              the depth in :attr:`redirect_max_depth`
                              (to intercept graph cycles)
        :raise ValueError: If no redirect found when following
                           ``redirect`` attributes, and silent
                           mode is not enabled.

        >>> from mock import Mock
        >>> entity = Mock()
        >>> entity.redirect.redirect = 'redirect_target'
        >>>
        >>> router = Router()
        >>> router.register(entity)
        >>>
        >>> pattern = router.get_redirect_pattern()
        >>>
        >>> type(pattern).__name__
        'RegexURLPattern'
        >>> pattern.callback.__name__
        'RedirectView'
        >>> pattern._target_url_name
        'redirect_target'

        >>> from mock import Mock
        >>> entity = Mock()
        >>> entity.redirect.redirect = 'redirect_target'
        >>>
        >>> router = Router()
        >>> router.register(entity)
        >>>
        >>> pattern = router.get_redirect_pattern(
        ...  namespaces=['ns1', 'ns2']
        ... )
        >>> type(pattern).__name__
        'RegexURLPattern'
        >>> pattern.callback.__name__
        'RedirectView'
        >>> pattern._target_url_name
        'ns1:ns2:redirect_target'

        >>> entity = Mock()
        >>> entity.redirect.redirect = entity
        >>>
        >>> router = Router()
        >>> router.register(entity)
        >>>
        >>> router.get_redirect_pattern()
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        OverflowError: Depth-first search reached its maximum (100)
        depth, without returning a leaf item (string).Maybe the
        redirect graph has a cycle ?

        >>> entity = Mock()
        >>> entity.__str__ = lambda x: 'mock redirect'
        >>> entity.redirect = None
        >>>
        >>> router = Router()
        >>> router.register(entity)
        >>>
        >>> router.get_redirect_pattern()
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        ValueError: Failed following redirect attribute (mock
        redirect) (last redirect found : mock redirect, redirect
        value: None)) in Router

        """
        # initialize default arguments
        if silent is None:
            silent = self.get_redirect_silent
        if redirect_max_depth is None:
            redirect_max_depth = self.redirect_max_depth
        if namespaces is None:
            namespaces = []
        else:
            # need to copy because _follow_redirect appends namespaces
            # found when following redirect attributes
            namespaces = list(namespaces)

        # used if following redirect attributes failed, to provide
        # information in the exception.
        _last_redirect_found = None

        redirect = self.redirect
        for i in range(redirect_max_depth):
            # loop through redirect attributes
            if isinstance(redirect, str):
                break
            elif redirect is None:
                break
            elif redirect is not None:
                # not a string and not None, check if it's a Router so
                # we can append its namespace to the namespaces list

                # maybe it's better to just getattr(redirect,
                # 'namespace') and to handle the exception (or
                # getattr(redirect, 'namespace', None))

                # can't decide either
                if isinstance(redirect, Router) and redirect.namespace:
                    namespaces.append(redirect.namespace)
                # save last redirect in case of exception
                _last_redirect_found = redirect
                # NOTE: risk of infinite loop here, if the redirect
                # attributes keeps being not None and never string
                # this could happen if case of "redirect loop" :
                # >>> A, B = [Router() for _ in range(3)]
                # >>> A.redirect = B
                # >>> B.redirect = A
                # >>> _follow_redirect(A)
                # --- /!\ infinite loop /!\ ---
                redirect = redirect.redirect
        else:
            raise OverflowError(
                "Depth-first search reached its maximum ({}) depth"
                ", without returning a leaf item (string)."
                "Maybe the redirect graph has a cycle ?"
                "".format(redirect_max_depth)
            )
        if redirect:
            # get the target URL name (by prefixing the redirect URL
            # name with the namespaces)
            target_url_name = ':'.join([
                ':'.join(namespaces),
                redirect,
            ]) if namespaces else redirect

            # Create an identifier for the redirection pattern.
            # This is not required as these patterns should not be
            # pointed to directly, but it helps when debugging
            # (use a random ID to avoid collisions)
            redirect_url_name = "{}-redirect".format(
                redirect,
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
            url_pattern._target_url_name = target_url_name

            return url_pattern
        elif not silent:
            # No URL found and set to fail (not silent) if we got
            # here, it's because _follow_redirect() returned
            # None.
            #
            # This will happen if self.redirect is None or if
            # following redirect attributes returned None somewhere
            raise ValueError(
                "Failed following redirect attribute ({}) "
                "(last redirect found : {}, redirect value: {})) in {}"
                "".format(
                    self.redirect,
                    _last_redirect_found,
                    getattr(_last_redirect_found, 'redirect', 'not defined'),
                    self.__class__.__name__
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
        :argument add_redirect: Override :attr:`Router.add_redirect`
        :type add_redirect: bool
        :argument add_redirect_silent: Override
                                       :attr:`Router.add_redirect_silent`
        :type add_redirect: bool

        >>> from mock import Mock
        >>> router = Router()
        >>> pattern = Mock()

        >>> entity_1 = Mock()
        >>> entity_1.index = False
        >>> entity_1.patterns = lambda *args: ['MockPattern1']
        >>>
        >>> router.register(entity_1)
        >>>
        >>> list(router.patterns())
        [<RegexURLResolver <str list> (None:None) ^>]
        >>> next(router.patterns()).url_patterns
        ['MockPattern1']

        >>> entity_2 = Mock()
        >>> entity_2.index = True
        >>> entity_2.redirect = 'redirect_target'
        >>> entity_2.patterns = lambda *args: ['MockPattern2']
        >>>
        >>> router.register(entity_2)
        >>>
        >>> list(router.patterns())
        ... # doctest: +NORMALIZE_WHITESPACE
        [<RegexURLResolver <RegexURLPattern list> (None:None) ^>]
        >>> next(router.patterns()).url_patterns
        ... # doctest: +NORMALIZE_WHITESPACE
        [<RegexURLPattern redirect_target-redirect ^$>,
         'MockPattern1', 'MockPattern2']

        >>> router.redirect = None
        >>>
        >>> list(router.patterns(add_redirect=True))
        ... # doctest: +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
          ...
        ValueError: No redirect attribute set (and
        ``add_redirect_silent`` is ``False``).
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
            if self.add_redirect is not None:  # pragma: no cover
                add_redirect = self.add_redirect
            else:
                add_redirect = bool(self.redirect)
        else:  # pragma: no cover
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
                            "No redirect attribute set "
                            "(and ``add_redirect_silent`` is ``False``)."
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

from .model import ModelRouter
from .model.generic import GenericModelRouter
