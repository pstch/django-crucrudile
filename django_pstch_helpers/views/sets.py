from . import ListView, DetailView, SearchView
from .multiple import MultipleListView
from .edit import CreateView, DeleteView, UpdateView 

PK_ARG = "(?P<pk>\d+)"

EDIT_VIEWS = { 'create' : ('create/%s',
                           CreateView,
                           {})
               'update' : ('update/%s' % PK_ARG,
                           UpdateView,
                           {}),
               'delete' : ('delete/%s' % PK_ARG,
                           DeleteView,
                           {}),
} 

LIST_VIEWS = { 'list' : ('list',
                         ListView,
                         {})
}

MULTIPLE_LIST_VIEWS = { 'list' : ('list',
                                  MultipleListView,
                                  {})
}

DETAIL_VIEWS = { 'detail': ('detail/%s' % PK_ARG,
                            DetailView,
                            {})
}

PAGINATED_LIST_VIEWS = { 'list' : ('list',
                                   ListView,
                                   { 'paginate_by' : lambda action, view, model: return model.PAGINATE_BY })
}

BASE_VIEWS = LIST_VIEWS + EDIT_VIEWS
FULL_VIEWS = BASE_VIEWS + DETAIL_VIEWS

SEARCH_VIEWS = { 'search' : ('search',
                             SearchView,
                             {})
}


