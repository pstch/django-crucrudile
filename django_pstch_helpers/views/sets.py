from . import ListView, DetailView, SearchView
from .multiple import MultipleListView
from .edit import CreateView, DeleteView, UpdateView 

PK_ARG = "(?P<pk>\d+)"

EDIT_VIEWS = [('create' , CreateView, None),
              ('update' , UpdateView, [PK_ARG, ]),
              ('delete' , DeleteView, [PK_ARG, ])]

LIST_VIEWS = [('list' , ListView, None),]
DETAIL_VIEWS = [('detail' , DetailView, [PK_ARG, ]),]

PAGINATED_LIST_VIEWS = [('list' , ListView, None),]

BASE_VIEWS = LIST_VIEWS + EDIT_VIEWS
FULL_VIEWS = BASE_VIEWS + DETAIL_VIEWS

SEARCH_VIEWS = [('search', SearchView, None),]

MULTIPLE_LIST_VIEWS = [('list' , MultipleListView, None),]
