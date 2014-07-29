""">>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.views.generic import TemplateView
>>> from django_crucrudile.routers import Router
>>> from django_crucrudile.routes import ViewRoute
>>>
>>> class HomeView(TemplateView):
...   pass
>>>
>>> class StatusView(TemplateView):
...   pass
>>>
>>> class HomeRoute(ViewRoute):
...   view_class = HomeView
>>>
>>> class StatusRoute(ViewRoute):
...   view_class = StatusView
>>>

>>>
... class HomeRouter(Router):
...   pass
>>>
>>> HomeRouter.register_class(HomeRoute) is HomeRoute
True
>>> HomeRouter.register_class(StatusRoute) is StatusRoute
True
>>>
>>> router = HomeRouter()
...
>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - HomeRouter  @ ^
   - home @ ^home$ HomeView
   - status @ ^status$ StatusView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^>]

As the instances that are automatically registered when the router is
instantiated may also be transformed by the register mappings, we can
even directly register the view class on the router :

>>>
... class HomeRouter(Router):
...   pass
>>>
>>> HomeRouter.register_class(lambda: HomeView) is not None
True
>>> HomeRouter.register_class(lambda: StatusView) is not None
True
>>>
>>> router = HomeRouter()

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - HomeRouter  @ ^
   - home @ ^home$ HomeView
   - status @ ^status$ StatusView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^>]

"""
