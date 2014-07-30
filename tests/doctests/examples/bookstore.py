"""Bookstore example, with three simple models.

>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.db.models import Model
>>> from django_crucrudile.routers import Router
>>>
>>>
>>> class Book(Model):
...   pass
>>>
>>> class Author(Model):
...   pass
>>>
>>> class Editor(Model):
...   pass

>>> router = Router(generic=True)
>>>
>>> router.register(Author, index=True) is not None
True
>>> router.register(Book) is not None
True
>>> router.register(Editor) is not None
True

>>> print(router.get_str_tree())
... # doctest: +NORMALIZE_WHITESPACE
 - Router  @ ^
   - author-list-redirect @ ^$ RedirectView
   - GenericModelRouter author @ ^author/
     - author-list-redirect @ ^$ RedirectView
     - author-delete @ ^delete/(?P<pk>\d+)$ DeleteView
     - author-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView
     - author-update @ ^update/(?P<pk>\d+)$ UpdateView
     - author-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
     - author-create @ ^create$ CreateView
     - author-detail @ ^detail/(?P<pk>\d+)$ DetailView
     - author-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
     - author-list @ ^list$ ListView
   - GenericModelRouter book @ ^book/
     - book-list-redirect @ ^$ RedirectView
     - book-delete @ ^delete/(?P<pk>\d+)$ DeleteView
     - book-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView
     - book-update @ ^update/(?P<pk>\d+)$ UpdateView
     - book-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
     - book-create @ ^create$ CreateView
     - book-detail @ ^detail/(?P<pk>\d+)$ DetailView
     - book-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
     - book-list @ ^list$ ListView
   - GenericModelRouter editor @ ^editor/
     - editor-list-redirect @ ^$ RedirectView
     - editor-delete @ ^delete/(?P<pk>\d+)$ DeleteView
     - editor-delete @ ^delete/(?P<slug>[\w-]+)$ DeleteView
     - editor-update @ ^update/(?P<pk>\d+)$ UpdateView
     - editor-update @ ^update/(?P<slug>[\w-]+)$ UpdateView
     - editor-create @ ^create$ CreateView
     - editor-detail @ ^detail/(?P<pk>\d+)$ DetailView
     - editor-detail @ ^detail/(?P<slug>[\w-]+)$ DetailView
     - editor-list @ ^list$ ListView
"""
