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


    .. testsetup::

       class ViewRoute(ViewMixin):
           pass

    """

    view_class = None
    """
    :attribute view_class: View class that will be used to get the
                           callback to pass to the URL pattern
    :type view_class: subclass of :class:`django.views.generic.view`
    """
    def __init__(self,
                 *args,
                 view_class=None,
                 **kwargs):
        """Initialize ViewRoute, check that view_class is defined at
        class-level or passed as argument.

        :argument view_class: See :attr:`view_class`

        :raises ValueError: if both ``view_class`` and
                            :attr:`view_class` are None

        .. testcode::

           view_class = type('TestView', (), {})
           route = ViewMixin(view_class=view_class)
           print(route.view_class.__name__)

        .. testoutput::

           TestView

        """
        if view_class is not None:
            self.view_class = view_class
        elif self.view_class is None:
            raise ValueError(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(**kwargs)

    def get_callback(self):
        """Return callback using :func:`django.generic.views.View.as_view`,
        getting arguments from :func:`get_view_kwargs`.

        Calls :func:`View.as_view` on view class, with kwargs from
        :func:`get_view_kwargs`, to get callback to use in URL
        pattern.

        :returns: Callback to use in URL pattern
        :rtype: callable

        .. testcode::

           callback = Mock()
           mock_view = Mock()
           mock_view.as_view = lambda: callback

           route = ViewRoute(view_class=mock_view)
           print(route.get_callback() is callback)

        .. testoutput::

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

        :returns: New class, with :attr:`view_class` attribute set to ``view_class`` argument.

        View class name ending with ``View`` :

        .. testcode::

           view_class = type('ListView', (), {})
           route_class = ViewMixin.make_for_view(
               view_class
           )
           print(route_class.__name__)
           print(route_class.name)
           print(route_class.view_class.__name__)

        .. testoutput::
           :options: +NORMALIZE_WHITESPACE

           ListRoute
           list
           ListView

        View class name **not** ending with ``View`` :

        .. testcode::

           view_class = type('FilteredList', (), {})
           route_class = ViewMixin.make_for_view(
               view_class
           )
           print(route_class.__name__)
           print(route_class.name)
           print(route_class.view_class.__name__)

        .. testoutput::
           :options: +NORMALIZE_WHITESPACE

           FilteredListRoute
           filteredlist
           FilteredList

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
