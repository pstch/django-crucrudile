from . import Route
from .view import ViewRoute


class ModelRoute(Route):
    """Implementation of Route that requires a model to be set either
    on the class (:attr:`model` attribute), or to be passed in
    :func:`__init__`.

    .. warning:: Abstract class ! Subclasses should define the
                 :func:`get_callback` function.

    .. inheritance-diagram:: ModelRoute
    """
    model = None
    """
    :attribute model: Model to use on the Route
    :type model: :class:`django.db.models.Model`
    """
    prefix_url_part = False
    """
    :attribute prefix_url_part: Prefix the URL part with the model
                                (ex: "/model/<url_part>")
    :type prefix_url_part: bool
    """
    def __init__(self,
                 model=None,
                 **kwargs):
        """Initialize ModelRoute, check that model is defined at class-level
        or passed as argument.

        """
        if model is not None:
            self.model = model
        elif self.model is None:
            raise ValueError(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(**kwargs)

    @property
    def model_url_name(self):
        """Return the model name to be used when building the URL name"""
        return self.model._meta.model_name

    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part"""
        return self.model_url_name

    def get_url_regexs(self, url_part=None):
        """Yield an URL part built using :class:`ModelRoute`
        :func:`model_url_part` and :class:`Route`
        :attr:`Route.url_part`.

        """
        if url_part is None:
            url_part = self.url_part

        if self.prefix_url_part:
            if self.url_part:
                url_part = "/".join(
                    [self.model_url_part, url_part]
                )
            else:
                url_part = self.model_url_part

        return super().get_url_regexs(url_part)

    def get_url_name(self):
        """Return the URL name built using :class:`ModelRoute`
        :func:`model_url_name` and :class:`Route`
        :attr:`Route.name`.

        """
        return "{}-{}".format(self.model_url_name, self.name)


class ModelViewRoute(ViewRoute, ModelRoute):
    """Combine :class:`ViewRoute` and :class:`ModelRoute` to make a view
    that can easily be used with a model and a generic view.

    Also provide :func:`make_for_view`, that helpes building
    subclasses of this class for a given view class.

    .. inheritance-diagram:: ModelViewRoute
    """
    def __init__(self, *args, **kwargs):
        # TODO: Experimental!
        super().__init__(*args, **kwargs)
        self.redirect = self.get_url_name()

    @classmethod
    def make_for_view(cls, view_class, **kwargs):
        """Return a subclass of this class, setting the ``view_class``
        argument at class-level.

        This is useful when combined with
        :func:`django_crucrudile.entity.store.EntityStore.register_class`,
        as it only accepts classes (in opposition to
        :func:`django_crucrudile.entity.store.EntityStore.register`).

        """
        view_name = view_class.__name__
        if view_name.endswith('View'):
            view_name = view_name[:-4]
        route_name = "{}Route".format(view_name)

        kwargs['view_class'] = view_class
        kwargs['name'] = view_name.lower()

        return type(
            route_name,
            (cls,),
            kwargs
        )

    def get_view_kwargs(self):
        """Make the view use :attr:`ModelRoute.model`.

        This is the effective combination of :class:`ModelRoute` and
        :class:`ViewRoute`.

        """
        return {'model': self.model}
