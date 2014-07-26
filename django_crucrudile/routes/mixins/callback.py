"""This module contains a route mixin, :class:`CallbackMixin`, that
implements :class:`django_crucrudile.routes.base.BaseRoute`.

"""
class CallbackMixin:
    """Route mixin, implements
    :class:`django_crucrudile.routes.base.BaseRoute`, requires a
    callback to be set either on the class (:attr:`callback`
    attribute), or to be passed in :func:`__init__`.

    .. note::

       This mixin makes the class concrete, as it implements the
       :func:`django_crucrudile.routes.base.BaseRoute.get_callback`
       abstract function.

    .. inheritance-diagram:: CallbackMixin

    """
    callback = None
    """
    :attribute callback: Callback that will be used by the URL pattern
    :type callback: callable
    """
    def __init__(self,
                 *args,
                 callback=None,
                 **kwargs):
        """Initialize CallbackRoute, check that callback is defined at
        class-level or passed as argument

        :argument callback: See :attr:`callback`

        :raises ValueError: If ``callback`` and :attr:`callback` are
                            both ``None``
        """
        if callback is not None:
            self.callback = callback
        elif self.callback is None:
                raise ValueError(
                    "No ``callback`` argument provided to __init__"
                    ", and no callback defined as class attribute."
                    " (in {})".format(self)
                )
        super().__init__(*args, **kwargs)

    def get_callback(self):
        """Return :attr:`callback`

        :returns: The callback set on class (:attr:`callback`) or
                  passed to :func:`__init__`.
        :rtype: callable"""
        return self.callback
