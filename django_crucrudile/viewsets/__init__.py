from django_crucrudile.routers import Router, ModelRouter

class ViewSet(object):
    router_class = Router
    """
    Base mixin for all viewsets
    """
    def get_router_kwargs(self):
        return {}

    def get_router(self):
        if self.router_class:
            return self.router_class(
                self.views,
                **self.get_router_kwargs()
            )

    def get_view_classes(self):
        """Return list of view classes for this viewset

        This function is overriden by viewset mixin classes, so
        that the view class list can be returned by get_views_classes()

        When overriden in a viewset mixin class, ``get_view_classes()`` should
        always get the upstream list of view classes using
        ``super(...).get_view_classes``) before appending a new view class.

        :return: View classes for this viewset
        :rtype: list

        """
        return []

    def get_args_by_view_class(self, view):
        """Return dict of keyword arguments for a view class

        This function is overriden by viewset mixin classes, to
        make available the dictionary of view arguments for each view
        used in this viewset, with ``get_args_by_view_class(view)``.

        When overriden in a viewset class or by the user,
        get_args_by_view should always get the current list of view
        classes using ``super(...).get_args_by_view_class``) before
        appending a new View. Usually, args are retrieved using super,
        then if the 'view_class' kwarg is the view class on which we
        want to set arguments, we update the args dictionary.

        :param view: View to get the args for
        :type view: view class

        :return: Arguments for view class given in ``view_class``, or empty dict
        :rtype: dict

        :raise ImproperlyConfigured: ``view_class`` not in
                                     ``self.get_view_classes()``

        """
        # pylint: disable=W0613
        if view_class not in self.get_view_classes():
            raise ImproperlyConfigured(
                "Tried to get the view arguments for a view class that is not"
                " defined by get_view_classes"
            )
        return {}

    def get_view_kwargs(self, view_class):
        return self.get_args_by_view_class(view_class)

    def get_view(self, view_class):
        kwargs = self.get_view_kwargs(view_class)
        return view.as_view(**kwargs)

    def get_views(self):
        return [
            self.get_view(view_class)
            for view_class in self.get_view_classes()
        ]

    views = property(get_views)

class ModelViewSet(ViewSet):
    router_class = ModelRouter

    def __init__(self, model):
        self.model = model

    def get_view_kwargs(self, view_class):
        kwargs = super(ModelViewSet, self).get_view_kwargs(view_class)
        kwargs['model'] = self.model
        return kwargs

    def get_router_kwargs(self):
        kwargs = super(ModelViewSet, self).get_router_kwargs()
        kwargs['model'] = self.model
        return kwargs
