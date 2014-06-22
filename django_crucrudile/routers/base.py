from abc import ABCMeta, abstractmethod, abstractproperty


class RoutedEntity(metaclass=ABCMeta):
    url_next_sep = ':'
    namespace = None

    def __init__(self, name=None, label=None, namespace=None):
        self.redirect = None
        self.name = name
        self.label = label
        self.namespace = namespace

    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        pass

    def get_redirect_url_name(self, parents=None, strict=None):
        def _url_full_name():
            for parent in parents + [self]:
                if parent.namespace is not None:
                    yield parent.namespace
                    yield parent.url_next_sep

            yield self.redirect or self.name

        return ''.join(_url_full_name())

    @abstractproperty
    def url_part(self):
        pass

    @property
    def redirect(self):
        return self._redirect

    @redirect.setter
    def redirect(self, value):
        self._redirect = value


class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class BaseRouter(RoutedEntity):
    pass


class BaseModelRouter(BaseRouter):
    pass
