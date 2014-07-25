from . import Route

class ViewRoute(Route):
    """Implementation of Route that requires a view class to be set either
    on the class (:attr:`view_class` attribute), or to be passed in
    :func:`__init__`.

    The view class will be used to get the callback to give to the URL
    pattern.

    .. inheritance-diagram:: ViewRoute
    """

    view_class = None
    """
    :attribute view_class: View class that will be used to get the
                           callback to pass to the URL pattern
    :type callback: :class:`django.views.generic.view`
    """
    def __init__(self,
                 view_class=None,
                 **kwargs):
        """Initialize ViewRoute, check that view_class is defined at
        class-level or passed as argument.

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
        getting arguments from :func:`get_view_kwargs`."""
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        """Return arguments to use to get the view callback."""
        return {}
