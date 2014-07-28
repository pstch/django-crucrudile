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
>>> class HelpView(TemplateView):
...   pass
>>>
>>> class VersionView(TemplateView):
...   pass

>>> router = Router()
>>>
>>> router.register(ViewRoute(HomeView), index=True)
>>> router.register(ViewRoute(StatusView))
>>>
>>> help_router = Router(url_part='help')
>>>
>>> help_router.register(ViewRoute(HelpView), index=True)
>>> help_router.register(ViewRoute(VersionView))
>>>
>>> router.register(help_router)

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - Router  @ ^
   - home-redirect @ ^$ RedirectView
   - home @ ^home$ HomeView
   - status @ ^status$ StatusView
   - Router  @ ^help/
     - help-redirect @ ^$ RedirectView
     - help @ ^help$ HelpView
     - version @ ^version$ VersionView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^>]

"""
