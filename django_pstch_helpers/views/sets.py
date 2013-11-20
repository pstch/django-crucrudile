from . import ListView, DetailView, SearchView, MultipleListView
from .edit import CreateView, DeleteView, UpdateView 

PK_ARG = "(?P<pk>\d+)"

EDIT_VIEWS = [ ('create' , CreateView, None , None),
               ('update' , UpdateView, [PK_ARG, ], None),
               ('delete' , DeleteView, [PK_ARG, ], None) ]

LIST_VIEWS = [ ('list' , ListView, None, None), ]
DETAIL_VIEWS = [ ('detail' , DetailView, [PK_ARG, ], None), ]


BASE_VIEWS = LIST_VIEWS + EDIT_VIEWS
FULL_VIEWS = BASE_VIEWS + DETAIL_VIEWS

SEARCH_VIEWS = [ ('search', SearchView, None, None), ]

MULTIPLE_LIST_VIEWS = [ ('list' , MultipleListView, None, None), ]
