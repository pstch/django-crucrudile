"""This module contains an :class:`AppRouter` class, which subclasses
:class:`django_crucrudile.routers.Router`. This class is initialized
with an application name, and automatically registers (when
initializing) entities it can found in the (by default) ``entities``
attribute of the application's ``router`` module.

"""
from importlib import import_module
from django.conf import settings

class AppMixin:
    """Router mixin that gets initialized with an application name, and
    automatically registers entities that :func:`get_routing_entities` can
    find in :func:`get_routing_module`. By defaults, this results to a
    lookup on the ``entities`` attribute of ``routing`` module of the
    given application.

    .. inheritance-diagram :: AppMixin
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
    add_app_url_part = True
    """
    :attribute add_app_namespace: Add application name as a part of
                                  the URL.
    :type add_app_namespace: bool
    """
    no_routing_module_silent = False
    """
    :attribute no_routing_module_silent: Don't fail if no routing
                                         module was found
    :type no_routing_module_silent: bool
    """
    no_app_entities_silent = True
    """
    :attribute no_app_entities_silent: Don't fail if the entities list
                                       loaded from the routing module
                                       is empty.
    :type no_app_entities_silent: bool
    """
    def __init__(self, app_module_name,
                 add_app_namespace=None,
                 add_app_url_part=None,
                 no_routing_module_silent=None,
                 no_app_entities_silent=None,
                 **kwargs):
        """Initialize application router, get namespace if required, run
        superclass init and load entities to register from module.

        :argument app_module_name: Application module name to
                                    load. Must be importable from
                                    project root.
        :type app_module_name: str
        :argument add_app_namespace: Override
                                      :attr:`add_app_namespace`
        :type add_app_namespace: bool or None
        """
        self.app_module_name = app_module_name
        if add_app_namespace is not None:
            self.add_app_namespace = add_app_namespace
        if add_app_url_part is not None:
            self.add_app_url_part = add_app_url_part
        if no_routing_module_silent is not None:
            self.no_routing_module_silent = no_routing_module_silent
        if no_app_entities_silent is not None:
            self.no_app_entities_silent = no_app_entities_silent

        if self.add_app_namespace:
            self.namespace = ':'.join(
                self.app_module_name.split('.')
            )
        if self.add_app_url_part:
            self.url_part = ''.join(
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

        :argument silent: Override :attr:`no_app_entities_silent`
        :type silent: bool or None

        """
        if silent is None:
            silent = self.no_app_entities_silent

        try:
            entities = self.get_routing_entities()
        except ImportError:
            if not self.no_routing_module_silent:
                raise
            else:
                return

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


class ProjectMixin:
    app_list = None
    add_project_namespace = None
    no_apps_silent = False
    """
    :attribute no_routing_module_silent: Don't fail if no routing
                                         module was found
    :type no_routing_module_silent: bool
    """
    no_routing_module_silent = True
    """
    :attribute no_routing_module_silent: Don't fail if no routing
                                         module was found
    :type no_routing_module_silent: bool
    """
    no_app_entities_silent = False
    """
    :attribute no_app_entities_silent: Don't fail if the entities list
                                       loaded from the routing module
                                       is empty.
    :type no_app_entities_silent: bool
    """
    def app_list_filter(self, app_name):
        return not app_name.startswith("django.")

    def get_settings_app_list(self):
        return [
            name for name in settings.INSTALLED_APPS
            if self.app_list_filter(name)
        ]

    @staticmethod
    def get_settings_project_name():
        return settings.PROJECT_APP_NAME

    def __init__(self,
                 app_list=None,
                 add_project_namespace=None,
                 no_routing_module_silent=None,
                 no_app_entities_silent=None,
                 **kwargs):
        if add_project_namespace is not None:
            self.add_project_namespace = add_project_namespace
        if self.add_project_namespace:
            self.namespace = self.get_settings_project_name()
        if no_routing_module_silent is not None:
            self.no_routing_module_silent = no_routing_module_silent
        if no_app_entities_silent is not None:
            self.no_app_entities_silent = no_app_entities_silent

        if app_list is not None:
            self.app_list = app_list
        else:
            self.app_list = self.get_settings_app_list()

        super().__init__(**kwargs)

        self.register_app_routers()

    def get_app_router(self, app_name):
        return self.app_router_class(
            app_name,
            no_routing_module_silent=self.no_routing_module_silent,
            no_app_entities_silent=self.no_app_entities_silent
        )

    def get_app_routers(self):
        return [
            self.get_app_router(app_name)
            for app_name in self.app_list
        ]

    def register_app_routers(self):
        routers = self.get_app_routers
        if routers:
            for router in routers:
                self.register(router)
        else:
            if not self.no_apps_silent:
                raise ValueError(
                    "ProjectRouter could not find any app router"
                    "(routers list empty, app list {})"
                    "".format(self.app_list)
                )
