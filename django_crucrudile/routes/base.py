from abc import abstractmethod

from django.conf.urls import url

from django_crucrudile.entity import RoutedEntity


class BaseRoute(RoutedEntity):
    name = None
    url_part = None
    auto_url_part = True

    def __init__(self, name=None, url_part=None):
        if name is not None:
            self.name = name
        elif self.name is None:
            raise Exception(
                "No ``name`` argument provided to __init__"
                ", and no name defined as class attribute."
                " (in {})".format(self)
            )
        if url_part is not None:
            self.url_part = url_part
        elif self.url_part is None:
            if self.auto_url_part:
                self.url_part = self.name
            else:
                raise Exception(
                    "No ``url_part`` argument provided to __init__"
                    ", and no url_part defined as class attribute."
                    " (in {})".format(self)
                )

    def patterns(self, *args, **kwargs):
        callback = self.get_callback()
        url_name = self.get_url_name()
        for url_part in self.get_url_parts():
            yield url(
                url_part,
                callback,
                url_name
            )

    @abstractmethod
    def get_callback(self):
        pass

    def get_url_parts(self):
        yield self.url_part

    def get_url_name(self):
        return self.name

class BaseViewRoute(BaseRoute):
    def __init__(self, view_class=None, name=None):
        super().__init__(name)
        if view_class is not None:
            self.view_class = view_class
        elif self.view_class is None:
            raise Exception(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )

class BaseModelRoute(BaseRoute):
    def __init__(self, model=None,
                 view_class=None, name=None):
        if model is not None:
            self.model = model
        elif self.model is None:
            raise Exception(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(view_class, name)
