"""Bookstore example, with three simple models.

>>> # these two lines are required to subclass Django model in doctests
>>> import tests.unit
>>> __name__ = "tests.doctests"

>>> from django.db.models import Model
>>> from django_crucrudile.routers import Router, ModelRouter
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
     - author-delete @ ^delete$ DeleteView
     - author-update @ ^update$ UpdateView
     - author-create @ ^create$ CreateView
     - author-detail @ ^detail$ DetailView
     - author-list @ ^list$ ListView
   - GenericModelRouter book @ ^book/
     - book-list-redirect @ ^$ RedirectView
     - book-delete @ ^delete$ DeleteView
     - book-update @ ^update$ UpdateView
     - book-create @ ^create$ CreateView
     - book-detail @ ^detail$ DetailView
     - book-list @ ^list$ ListView
   - GenericModelRouter editor @ ^editor/
     - editor-list-redirect @ ^$ RedirectView
     - editor-delete @ ^delete$ DeleteView
     - editor-update @ ^update$ UpdateView
     - editor-create @ ^create$ CreateView
     - editor-detail @ ^detail$ DetailView
     - editor-list @ ^list$ ListView

"""
