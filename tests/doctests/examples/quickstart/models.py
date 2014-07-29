""">>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.views.generic import ListView, DetailView, TemplateView
>>> from django.db.models import Model
>>> from django_crucrudile.routers import Router, ModelRouter
>>> from django_crucrudile.routes import ViewRoute, ModelViewRoute
>>>
>>> class HomeView(TemplateView):
...   pass
>>>
>>> class Book(Model):
...   pass
>>>
>>> class BookListRoute(ModelViewRoute):
...    model = Book
...    view_class = ListView
>>>
>>> class BookDetailRoute(ModelViewRoute):
...    model = Book
...    view_class = DetailView

>>> router = Router()
>>>
>>> router.register(ViewRoute(HomeView)) is not None
True
>>>
>>> books_router = ModelRouter(Book)
>>>
>>> books_router.register(BookListRoute()) is not None
True
>>> books_router.register(BookDetailRoute()) is not None
True
>>>
>>> router.register(books_router) is books_router
True

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - Router  @ ^
   - home @ ^home$ HomeView
   - ModelRouter book @ ^book/
     - book-list @ ^list$ ListView
     - book-detail @ ^detail$ DetailView

>>> list(router.patterns())
[<RegexURLResolver <RegexURLPattern list> (None:None) ^>]
"""
