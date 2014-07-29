"""
>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.views.generic import TemplateView, ListView
>>> from django.db.models import Model
>>> from django_crucrudile.routers import Router
>>>
>>> class HomeView(TemplateView):
...   pass
>>>
>>> class StatusView(TemplateView):
...   pass
>>>
>>> class HelpView(TemplateView):
...   pass
>>>
>>> class VersionView(TemplateView):
...   pass
>>>
... class TestModel(Model):
...   pass
>>>

>>> router = Router()
>>>
>>> router.register(HomeView) is not None
True
>>> router.register(StatusView) is not None
True
>>>
>>> router.register(
...   ListView,
...   map_kwargs=dict(
...     model=TestModel,
...     prefix_url_part=True
...   )
... ) is not None
True
>>>
>>> help_router = Router(url_part='help')
>>>
>>> help_router.register(HelpView) is not None
True
>>> help_router.register(
...   VersionView,
...   map_kwargs=dict(name='app-version')
... ) is not None
True
>>>
>>> router.register(help_router) is help_router
True

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - Router  @ ^
   - home @ ^home$ HomeView
   - status @ ^status$ StatusView
   - testmodel-list @ ^testmodel/list$ ListView
   - Router  @ ^help/
     - help @ ^help$ HelpView
     - app-version @ ^app-version$ VersionView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^>]

"""
