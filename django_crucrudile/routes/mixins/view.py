"""This module contains a route mixin, :class:`ViewMixin`, that
implements :class:`django_crucrudile.routes.base.BaseRoute`.

"""


class ViewMixin:
    """Route mixin, implements
    :class:`django_crucrudile.routes.base.BaseRoute`, requires a
    view class to be set either on the class (:attr:`callback`
    attribute), or to be passed in :func:`__init__`.

    The view class will be used to get the callback to give to the URL
    pattern.

    .. note::

       This mixin makes the class concrete, as it implements the
       :func:`django_crucrudile.routes.base.BaseRoute.get_callback`
       abstract function.

    .. inheritance-diagram:: ViewMixin

    >>> class TestView:
    ...   pass
    >>>
    >>> route = ViewMixin(TestView)
    >>>
    >>> route.view_class.__name__
    'TestView'
    >>> route.name
    'test'

    With :attr:`auto_url_name_from_view` set to ``False`` :

    >>> class TestView:
    ...   pass
    >>>
    >>> route = ViewMixin(TestView, auto_url_name_from_view=False)
    >>>
    >>> route.view_class.__name__
    'TestView'
    >>>
    >>> # Because :class:`ViewMixin` does not even set
    >>> # :attr:`django_crucrudile.routes.base.BaseRoute.name` if
    >>> # :attr:`auto_url_name_from_view` is ``False``, this will
    >>> # raise an attribute error :
    >>> route.name
    Traceback (most recent call last):
      ...
    AttributeError: 'ViewMixin' object has no attribute 'name'

    """

    view_class = None
    """
    :attribute view_class: View class that will be used to get the
                           callback to pass to the URL pattern
    :type view_class: subclass of :class:`django.views.generic.view`
    """
    auto_url_name_from_view = True
    """
    :attribute auto_url_name_from_view: Automatically set route name using view
                                        class name (lower casing it, and
                                        stripping it of ``View``)
    :type auto_url_name_from_view: bool
    """
    def __init__(self,
                 view_class=None,
                 name=None,
                 auto_url_name_from_view=None,
                 *args,
                 **kwargs):
        """Initialize ViewRoute, check that view_class is defined at
        class-level or passed as argument.

        :argument view_class: See :attr:`view_class`
        :argument auto_url_name_from_view: See :attr:`auto_url_name_from_view`

        .. seealso::

           For doctests that use this member, see
           :class:`ViewMixin`

        :raises ValueError: if both ``view_class`` and
                            :attr:`view_class` are None

        """
        if view_class is not None:
            self.view_class = view_class
        if auto_url_name_from_view is not None:
            self.auto_url_name_from_view = auto_url_name_from_view
        elif self.view_class is None:  # pragma: no cover
            raise ValueError(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )
        if name is not None:
            kwargs['name'] = name
        elif self.auto_url_name_from_view:
            view_name = self.view_class.__name__
            if view_name.endswith('View'):
                view_name = view_name[:-4]
            self.name = view_name.lower()

        super().__init__(**kwargs)

    def get_callback(self):
        """Return callback using :func:`django.generic.views.View.as_view`,
        getting arguments from :func:`get_view_kwargs`.

        Calls :func:`View.as_view` on view class, with kwargs from
        :func:`get_view_kwargs`, to get callback to use in URL
        pattern.

        :returns: Callback to use in URL pattern
        :rtype: callable

        >>> from mock import Mock
        >>> callback = Mock()
        >>> mock_view = Mock()
        >>> mock_view.__name__ = 'MockView'
        >>> mock_view.as_view = lambda: callback
        >>>
        >>> route = ViewMixin(view_class=mock_view)
        >>> route.get_callback() is callback
        True

        """
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        """Return arguments to use when calling the callback builder.

        :returns: Keyword arguments
        :rtype: dict
        """
        return {}

    @classmethod
    def make_for_view(cls, view_class, **kwargs):
        """Return a subclass of this class, setting the ``view_class``
        argument at class-level.

        Also sets the
        :attr:`django_crucrudile.routes.base.BaseRoute.name` attribute
        using the view class name.

        This is useful when combined with
        :func:`django_crucrudile.entities.store.EntityStore.register_class`,
        as it only accepts classes (in opposition to
        :func:`django_crucrudile.entities.store.EntityStore.register`).

        :argument view_class: View class to set on the resulting class
        :type view_class: subclass of :class:`django.views.generic.view`

        :returns: New class, with :attr:`view_class` attribute set to
                  ``view_class`` argument.

        >>> class TestView:
        ...   pass
        >>>
        >>> route_class = ViewMixin.make_for_view(TestView)
        >>>
        >>> route_class.__name__
        'TestRoute'
        >>> route_class.view_class.__name__
        'TestView'

        """
        view_name = view_class.__name__
        if view_name.endswith('View'):
            view_name = view_name[:-4]
        route_name = "{}Route".format(view_name)

        kwargs['view_class'] = view_class

        return type(
            route_name,
            (cls,),
            kwargs
        )
