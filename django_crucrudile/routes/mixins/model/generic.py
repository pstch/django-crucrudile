"""This module contains :class:`GenericViewArgsMixin`, a route mixin
that can be used to automatically get the needed URL arguments for a
Django generic view.

"""
from itertools import chain
from django.views.generic import (
    DetailView, UpdateView, DeleteView
)


class GenericViewArgsMixin:
    """This route mixin, that should be used with
    :class:`django_crucrudile.routes.mixins.arguments.ArgumentsMixin` and
    :class:`django_crucrudile.routes.mixins.view.ViewMixin`,
    enables automatic URL arguments for Django generic views.

    """
    def get_view_arguments(self):
        """Return URL arguments if the view class is a Django generic view
        that requires an URL argument for the object.

        :returns: View argument specification
        :rtype: iterable

        """
        if issubclass(
                self.view_class,
                (DetailView, UpdateView, DeleteView)
        ):
            yield [r"(?P<pk>\d+)", r"(?P<slug>[\w-]+)"]

    def get_arguments_spec(self):
        """Add view arguments (returned by :func:`get_view_arguments`) to the
        arguments specification returned by the super implementation
        (:func:`django_crucrudile.routes.mixins.arguments.ArgumentsMixin.get_arguments_spec`).

        :returns: Arguments specification
        :rtype: iterable
        """
        return chain(
            super().get_arguments_spec(),
            self.get_view_arguments()
        )
