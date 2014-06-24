from abc import ABCMeta, abstractmethod, abstractproperty


class RoutedEntity(metaclass=ABCMeta):
    """Abstract class for routed entities

    Subclasses should define the ``patterns()`` method, that should
    return a generator yielding Django URL objects (RegexURLPattern or
    RegexURLResolver).

    """
    index = False
    """
    :attribute index: Used when routed entity is registered, to know if
                      it should be registered as index.
    :type index: bool
    """

    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        pass


class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class BaseRouter(RoutedEntity):
    pass


class BaseModelRouter(BaseRouter):
    pass
