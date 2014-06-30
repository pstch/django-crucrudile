from importlib import import_module
from . import Router


class AppRouter(Router):
    routing_module_name = "routing"
    entities_attribute_name = "entities"
    add_app_namespace = True
    register_app_silent = True

    def __init__(self, app_module_name, add_app_namespace=None, **kwargs):
        self.app_module_name = app_module_name
        if add_app_namespace is None:
            add_app_namespace = self.add_app_namespace

        if add_app_namespace:
            self.namespace = ':'.join(
                self.app_module_name.split('.')
            )

        super().__init__(**kwargs)

        self.register_module_entities()

    def get_routing_module_path(self):
        return '.'.join([
            self.app_module_name,
            self.routing_module_name
        ])


    def get_routing_module(self):
        return import_module(
            self.get_routing_module_path()
        )

    def get_routing_entities(self):
        return getattr(
            self.get_routing_module(),
            self.entities_attribute_name
        )

    def register_module_entities(self, silent=None):
        if silent is None:
            silent = self.register_app_silent

        entities = self.get_routing_entities()
        if entities:
            for entity in entities:
                self.register(entity)

        elif not silent:
            raise ValueError(
                "'{}' attribute not set (or empty) on {}"
                "".format(
                    self.routing_module_name,
                    self.get_routing_module_path()
                )
            )
