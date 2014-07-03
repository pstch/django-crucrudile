Books example
=============

.. testsetup:: *

   import tests.doctests

   from django.db import models
   from django_crucrudile.routers import Router, ModelRouter

   __name__ = "tests.doctests"

   class Book(models.Model):
       ...

   class Author(models.Model):
       ...

   class Editor(models.Model):
       ...

.. doctest::
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   >>> router = Router()

   >>> router.register(Author, index=True)
   >>> router.register(Book)
   >>> router.register(Editor)

   >>> print(router.get_str_tree())
    - Router  @ ^
      - author-list-redirect @ ^$ RedirectView
      - ModelRouter author @ ^author/
        - author-list-redirect @ ^$ RedirectView
        - author-delete @ ^delete$ DeleteView
        - author-update @ ^update$ UpdateView
        - author-create @ ^create$ CreateView
        - author-detail @ ^detail$ DetailView
        - author-list @ ^list$ ListView
      - ModelRouter book @ ^book/
        - book-list-redirect @ ^$ RedirectView
        - book-delete @ ^delete$ DeleteView
        - book-update @ ^update$ UpdateView
        - book-create @ ^create$ CreateView
        - book-detail @ ^detail$ DetailView
        - book-list @ ^list$ ListView
      - ModelRouter editor @ ^editor/
        - editor-list-redirect @ ^$ RedirectView
        - editor-delete @ ^delete$ DeleteView
        - editor-update @ ^update$ UpdateView
        - editor-create @ ^create$ CreateView
        - editor-detail @ ^detail$ DetailView
        - editor-list @ ^list$ ListView
