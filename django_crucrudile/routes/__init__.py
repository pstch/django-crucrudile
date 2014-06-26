from abc import abstractmethod

from django.conf.urls import url

from django_crucrudile.entity import Entity


class Route(Entity):
    name = None
    url_part = None
    auto_url_part = True

    def __init__(self, *args,
                 name=None, url_part=None,
                 **kwargs):
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
                    ", no url_part defined as class attribute."
                    " (in {}), and auto_url_part is set to False."
                    "".format(self)
                )
        super().__init__(*args, **kwargs)

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


class CallbackRoute(Route):
    callback = None

    def __init__(self, *args,
                 callback=None,
                 **kwargs):
        if callback is not None:
            self.callback = None
        elif self.callback is None:
                raise Exception(
                    "No ``callback`` argument provided to __init__"
                    ", and no callback defined as class attribute."
                    " (in {})".format(self)
                )
        super().__init__(*args, **kwargs)

    def get_callback(self):
        return self.callback


class ViewRoute(Route):
    view_class = None

    def __init__(self, *args,
                 view_class=None,
                 **kwargs):
        if view_class is not None:
            self.view_class = view_class
        elif self.view_class is None:
            raise Exception(
                "No ``view_class`` argument provided to __init__"
                ", and no view_class defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(*args, **kwargs)

    def get_callback(self):
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        return {}


class ModelRoute(Route):
    def __init__(self, *args,
                 model=None,
                 **kwargs):
        if model is not None:
            self.model = model
        elif self.model is None:
            raise Exception(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(*args, **kwargs)

    @property
    def model_url_part(self):
        return self.model._meta.model_name

    @property
    def model_url_name(self):
        return self.model._meta.model_name

    def get_url_parts(self):
        yield "^{}/{}$".format(self.model_url_part, self.url_part)

    def get_url_name(self):
        return "{}-{}".format(self.model_url_name, self.name)


class ModelViewRoute(ViewRoute, ModelRoute):
    @classmethod
    def make_for_view(cls, view_class, **kwargs):
        view_name = view_class.__name__
        if view_name.endswith('View'):
            view_name = view_name[:-4]
        route_name = "{}Route".format(view_name)

        kwargs['view_class'] = view_class
        kwargs['name'] = view_name.lower()

        return type(
            route_name,
            (cls,),
            kwargs
        )

    def get_view_kwargs(self):
        return {'model': self.model}
