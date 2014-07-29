"""
>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.views.generic import TemplateView
>>> from django_crucrudile.routers import Router, ViewRoute
>>>
>>> class HomeView(TemplateView):
...   pass
>>>
>>> class StatusView(TemplateView):
...   pass
>>>
>>> router = Router()
>>>
>>> router.register(ViewRoute(HomeView)) is not None
True
>>> router.register(
...   ViewRoute(
...     StatusView,
...     arguments_spec=[["<pk>", "<slug>"], (False, "<format>")]
...   )
... ) is not None
True

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - Router  @ ^
   - home @ ^home$ HomeView
   - status @ ^status/<pk>/?<format>$ StatusView
   - status @ ^status/<slug>/?<format>$ StatusView

"""
