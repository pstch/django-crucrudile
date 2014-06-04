from collections import defaultdict

from django_crucrudile.routers import Router, ModelRouter

class ViewDefinition:
    def __init__(self, action=None, view_class, view_args=None, url_args=None):
        self.action = action
        self.view_class = view_class
        self.view_args = view_args or {}
        self.url_args = url_args or []

class ViewSet:
    router_class = Router

    def __init__(self):
        self._definitions = {}

    @property
    def viewdefs(self):
        return self._definitions.values() or []

    @definitions.setter
    def set_viewdefs(self, value):
        self._definitions = {d.action : d for d in value}

    def set_viewdef(self, definition):
        self._definitions[definition.action] = definition

    def get_viewdef(self, action):
        return self._definitions[action]

        def get_router

    def get_router_kwargs(self):
        return {}

    def get_router(self):
        if self.router_class:
            return self.router_class(
                self.make_views(),
                **self.get_router_kwargs()
            )

    def make_views(self):
        return [
            view_class.as_view(**view_args)
            for view_class, view_args  in self.items()
        ]

class ModelViewSet(ViewSet):
    router_class = ModelRouter

    def __init__(self, model):
        self.model = model
        self.default = lambda: {'model': model}

    def get_router_kwargs(self):
        kwargs = super(ModelViewSet, self).get_router_kwargs()
        kwargs['model'] = self.model
        return kwargs
