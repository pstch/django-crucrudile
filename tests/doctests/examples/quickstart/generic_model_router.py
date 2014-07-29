"""
>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"
>>>
>>> from django.db.models import Model
>>> from django.views.generic import (
...     ListView, DetailView,
...     CreateView, UpdateView, DeleteView
... )
>>> from django_crucrudile.routers.model import ModelRouter
>>>
>>> class TestModel(Model):
...   pass
>>>
>>> class GenericModelRouter(ModelRouter):
...   pass

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
   - testmodel-detail @ ^detail$ DetailView
   - testmodel-create @ ^create$ CreateView
   - testmodel-update @ ^update$ UpdateView
   - testmodel-delete @ ^delete$ DeleteView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^testmodel/>]

"""
