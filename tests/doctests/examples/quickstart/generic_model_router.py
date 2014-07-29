"""
>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"
>>>
>>> from django.db.models import Model
>>> from django.views.generic.detail import SingleObjectMixin
>>> from django.views.generic.list import MultipleObjectMixin
>>> from django.views.generic import (
...     ListView, DetailView,
...     CreateView, UpdateView, DeleteView
... )
>>> from django_crucrudile.routers import ModelRouter
>>> from django_crucrudile.routes import GenericModelViewRoute
>>>
>>> class TestModel(Model):
...   pass
>>>
>>> class GenericModelRouter(ModelRouter):
...   @classmethod
...   def get_register_class_map(cls):
...     mapping = super().get_register_class_map()
...     mapping[SingleObjectMixin, MultipleObjectMixin] = (
...       GenericModelViewRoute.make_for_view
...     )
...     return mapping

>>> GenericModelRouter.register_class(
...   ListView, map_kwargs={'index': True}
... ) is not None
True
>>> GenericModelRouter.register_class(DetailView) is not None
True
>>> GenericModelRouter.register_class(CreateView) is not None
True
>>> GenericModelRouter.register_class(UpdateView) is not None
True
>>> GenericModelRouter.register_class(DeleteView) is not None
True

>>> router = GenericModelRouter(TestModel)

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - GenericModelRouter testmodel @ ^testmodel/
   - testmodel-list-redirect @ ^$ RedirectView
   - testmodel-list @ ^list$ ListView
   - testmodel-detail @ ^detail/(?P<pk>\d+)$ DetailView
   - testmodel-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
   - testmodel-create @ ^create$ CreateView
   - testmodel-update @ ^update/(?P<pk>\d+)$ UpdateView
   - testmodel-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
   - testmodel-delete @ ^delete/(?P<pk>\d+)$ DeleteView
   - testmodel-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^testmodel/>]

"""
