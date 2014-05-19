class ViewSet(object):
    router_class = None
    """
    Base mixin for all viewsets
    """
    def __init__(self, model):
        self.model = model

    def get_router(self):
        if self.router_class:
            return self.router_class(self)

    @classmethod
    def get_views(cls):
        """Return list of views for this viewset

        This class method is overriden by viewset mixin classes, so
        that the view list can be returned by get_views()

        When overriden in a viewset mixin class, ``get_views()`` should
        always get the upstream list of views using
        ``super(...).get_views``) before appending a new view.

        :return: Views for this viewset
        :rtype: list

        """
        return []

    @classmethod
    def get_args_by_view(cls, view):
        """Return dict of keyword arguments for a view

        This class method is overriden by viewset mixin classes, so that the
        resulting Model object (which subclasses viewset mixin classes)
        can get the dictionary of view arguments for each view used in
        this viewset, with ``get_args_by_view(view)``.

        When overriden in a viewset class or by the user,
        get_args_by_view should always get the current list of views
        using ``super(...).get_views``) before appending a new
        View. Usually, args are  retrieved using super, then if the
        'view' kwarg is the view on which we want to set arguments, we
        update the args dictionary.

        :param view: View to get the args for
        :type view: view class

        :return: Arguments for view given in ``view``, or empty dict
        :rtype: dict

        :raise ImproperlyConfigured: ``view`` not in ``cls.get_views()``

        """
        # pylint: disable=W0613
        if view not in cls.get_views():
            raise ImproperlyConfigured(
                "Tried to get the view arguments for a view that is not"
                " defined by get_views"
            )
        return {}
