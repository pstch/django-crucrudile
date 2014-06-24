from abc import ABCMeta, abstractmethod, abstractproperty


class RoutedEntity(metaclass=ABCMeta):
    index = False
    name = None
    namespace = None
    label = None
    url_part = None

    def __init__(self, name=None, label=None,
                 namespace=None, url_part=None):
        self.redirect = None
        if name is not None:
            self.name = name
        if label is not None:
            self.label = label
        if namespace is not None:
            self.namespace = namespace
        if url_part is not None:
            self.url_part = url_part
        elif self.url_part is None:
            self.url_part = ''

    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                    namespace=None, name=None,
                    entity=None, add_redirect=True):
        pass

    def get_redirect_url_name(self, parents=None, strict=None):
        return ''.join(
            [
                ''.join([parent.namespace, ':'])
                for parent in parents + [self]
                if parent.namespace is not None
            ] + [
                self.redirect or self.name
            ]
        )

class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class BaseRouter(RoutedEntity):
    pass


class BaseModelRouter(BaseRouter):
    pass
