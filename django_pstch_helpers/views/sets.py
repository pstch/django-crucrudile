from . import ListView, DetailView, SearchView
from .multiple import MultipleListView
from .edit import CreateView, DeleteView, UpdateView 

PK_ARG = "(?P<pk>\d+)"
FILTER_ARGS = "of-(?P<filter_key>\w+)/(?P<filter_value>\d+)"

EDIT_VIEWS = { 'create' : ('create',
                           CreateView,
                           {}),
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
FILTERED_LIST_VIEWS = { 'list' : ('list/%s' % FILTER_ARGS,
                                  FilteredListView,
                                  {}),
                    }

DETAIL_VIEWS = { 'detail': ('detail/%s' % PK_ARG,
                            DetailView,
                            {})
             }

PAGINATED_LIST_VIEWS = { 'list' : ('list',
                                   ListView,
                                   lambda action, view, model: { 'paginate_by' : getattr(model,
                                                                                         'PAGINATE_BY',
                                                                                         50) })
}

BASE_VIEWS = dict(LIST_VIEWS,
                  **EDIT_VIEWS)

FULL_VIEWS = dict(BASE_VIEWS,
                  **DETAIL_VIEWS)

SEARCH_VIEWS = { 'search' : ('search',
                             SearchView,
                             {})
}


