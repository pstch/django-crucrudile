"""This module contains an :class:`AppRouter` class, which subclasses
:class:`django_crucrudile.routers.Router`. This class is initialized
with an application name, and automatically registers (when
initializing) entities it can found in the (by default) ``entities``
attribute of the application's ``router`` module.

"""
from importlib import import_module
from . import Router


class AppRouter(Router):
    """Router that gets initialized with an application name, and
    automatically registers entities that :func:`get_routing_entities` can
    find in :func:`get_routing_module`. By defaults, this results to a
    lookup on the ``entities`` attribute of ``routing`` module of the
    given application.

    """
    routing_module_name = "routing"
    """
    :attribute routing_module_name: Module to load in application, in
                                    order to get the entities.
    :type routing_module_name: str
    """
    entities_attribute_name = "entities"
    """
    :attribute entities_attribute_name: Attribute to use when looking
                                        for entities in the routing
                                        module.
    :type entities_attribute_name: str
    """
    add_app_namespace = True
    """
    :attribute add_app_namespace: Add application name as a namespace.
    :type add_app_namespace: bool
    """
    no_app_entities_silent = True
    """
    :attribute no_app_entities_silent: Don't fail if the entities list
                                       loaded from the routing module
                                       is empty.
    :type no_app_entities_silent: bool
    """
    def __init__(self, app_module_name, add_app_namespace=None, **kwargs):
        """Initialize application router, get namespace if required, run
        superclass init and load entities to register from module.

        :attribute app_module_name: Application module name to
                                    load. Must be importable from
                                    project root.
        :type app_module_name: str
        :attribute add_app_namespace: Override
                                      :attr:`add_app_namespace`
        :type add_app_namespace: bool or None
        """
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
        """Get routing module path (compiled from application name given in
        :func:`__init__` and :attr:`routing_module_name`)

        """
        return '.'.join([
            self.app_module_name,
            self.routing_module_name
        ])


    def get_routing_module(self):
        """Load routing module using path from
        :func:`get_routing_module_path`.

        """
        return import_module(
            self.get_routing_module_path()
        )

    def get_routing_entities(self):
        """Get entities using module from :func:`get_routing_module` and
        attribute name from :attr:`self.entities_attribute_name`.

        """
        return getattr(
            self.get_routing_module(),
            self.entities_attribute_name
        )

    def register_module_entities(self, silent=None):
        """Register entities returned by :func:`self.get_routing_entities`.

        :attribute silent: Override :attr:`no_app_entities_silent`
        :type silent: bool or None

        """
        if silent is None:
            silent = self.no_app_entities_silent

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
