from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from django_crucrudile.entities.store import provides
from django_crucrudile.routes import GenericModelViewRoute

from . import ModelRouter


@provides(ListView, map_kwargs={'index': True})
@provides(DetailView)
@provides(CreateView)
@provides(UpdateView)
@provides(DeleteView)
class GenericModelRouter(ModelRouter):
    """Generic model router, subclasses
    :class:`django_crucrudile.routers.model.ModelRouter` and use 5 Django
    generic views for each registered model.

    Provides specific :class:`django_crucrudile.routes.ModelViewRoute`
    classes, created for the following Django generic views :

     - :class:`django.views.generic.ListView`
     - :class:`django.views.generic.DetailView`
     - :class:`django.views.generic.CreateView`
     - :class:`django.views.generic.UpdateView`
     - :class:`django.views.generic.DeleteView`

    These classes are registered in the base store, using
    :func:`django_crucrudile.entities.store.EntityStore.register_class`
    or the :func:`django_crucrudile.entities.store.provides`
    decorator. They will be instantiated (with the model as argument)
    when the router is itself instantiated, using
    :func:`django_crucrudile.entities.store.EntityStore.register_base_store`.

    We use our own class mapping, to use our own route, because we
    want to add the arguments specification to the route
    automatically.

    .. inheritance-diagram:: GenericModelRouter

    >>> # these two lines are required to subclass Django model in doctests
    >>> import tests.unit
    >>> __name__ = "tests.doctests"
    >>> from django.db.models import Model
    >>> from django_crucrudile.routers import Router, ModelRouter
    >>>
    >>> class TestModel(Model):
    ...   pass

    >>> router = Router(generic=True)
    >>>
    >>> router.register(TestModel) is not None
    True

    >>> print(router.get_str_tree())
    ... # doctest: +NORMALIZE_WHITESPACE
     - Router  @ ^
       - GenericModelRouter testmodel @ ^testmodel/
         - testmodel-list-redirect @ ^$ RedirectView
         - testmodel-delete @ ^delete/(?P<pk>\d+)$ DeleteView
         - testmodel-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView
         - testmodel-update @ ^update/(?P<pk>\d+)$ UpdateView
         - testmodel-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
         - testmodel-create @ ^create$ CreateView
         - testmodel-detail @ ^detail/(?P<pk>\d+)$ DetailView
         - testmodel-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
         - testmodel-list @ ^list$ ListView

    """
    @classmethod
    def get_register_class_map(cls):
        """Override super implementation to set the mapping for Django generic
        views to
        :class:`django_crucrudile.routes.GenericModelViewRoute`.

           For doctests that use this member, see
           :class:`django_crucrudile.routers.model.generic.GenericModelRouter`

        """
        mapping = super().get_register_class_map()
        mapping[SingleObjectMixin, MultipleObjectMixin] = (
            GenericModelViewRoute.make_for_view
        )
        return mapping
