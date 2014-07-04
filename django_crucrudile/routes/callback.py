from . import Route


class CallbackRoute(Route):
    """Implementation of Route that requires a callback to be set either
    on the class (:attr:`callback` attribute), or to be passed in
    :func:`__init__`.

    .. inheritance-diagram:: CallbackRoute
    """
    callback = None
    """
    :attribute callback: Callback that will be used by the URL pattern
    :type callback: callable
    """
    def __init__(self,
                 callback=None,
                 **kwargs):
        """Initialize CallbackRoute, check that callable is defined at
        class-level or passed as argument

        """
        if callback is not None:
            self.callback = callback
        elif self.callback is None:
                raise ValueError(
                    "No ``callback`` argument provided to __init__"
                    ", and no callback defined as class attribute."
                    " (in {})".format(self)
                )
        super().__init__(**kwargs)

    def get_callback(self):
        """Return :attr:`callback`"""
        return self.callback
