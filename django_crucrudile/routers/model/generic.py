from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from django_crucrudile.entities.store import provides


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

    .. inheritance-diagram:: GenericModelRouter

    """
