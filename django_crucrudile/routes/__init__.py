from django.views.generic import (
    View,
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)


from .base import (
    BaseRoute, BaseViewRoute, BaseModelRoute,
)


class ViewRoute(BaseViewRoute):
    """
    .. inheritance-diagram:: ViewRoute
    """
    view_class = None

    def get_callback(self):
        return self.view_class.as_view(
            **self.get_view_kwargs()
        )

    def get_view_kwargs(self):
        return {}

class ModelRoute(BaseModelRoute, ViewRoute):
    """
    .. inheritance-diagram:: ModelRoute
    """
    def get_view_kwargs(self):
        return {'model': self.model}

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


class ListRoute(ModelRoute):
    name = "list"
    view_class = ListView
    index = True


class DetailRoute(ModelRoute):
    name = "detail"
    view_class = DetailView


class CreateRoute(ModelRoute):
    name = "create"
    view_class = CreateView


class UpdateRoute(ModelRoute):
    name = "update"
    view_class = UpdateView


class DeleteRoute(ModelRoute):
    name = "delete"
    view_class = DeleteView
