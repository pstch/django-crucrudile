-from . import ListView, DetailView, SearchView
from .multiple import MultipleListView
from .edit import CreateView, DeleteView, UpdateView 
from .filtered import FilteredListView
from .specific import SpecificCreateView
PK_ARG = "(?P<pk>\d+)"
FILTER_ARGS = "of-(?P<filter_key>\w+)/(?P<filter_value>\d+)"
SPECIFIC_ARGS = "of-(?P<specific_key>\w+)/(?P<specific_value>\d+)"


CREATE_VIEW = { 'create' : ('create',
                           CreateView,
                           {})}

SPECIFIC_CREATE_VIEW = { 'create' : ('create/of-%s' % SPECIFIC_ARGS,
                         SpecificCreateView,
                         {}),}

UPDATE_VIEW =  { 'update' : ('update/%s' % PK_ARG,
                             UpdateView,
                             {}),}
DELETE_VIEW = { 'delete' : ('delete/%s' % PK_ARG,
                           DeleteView,
                           {}),}

LIST_VIEW = { 'list' : ('list',
                         ListView,
                         {})
           }

MULTIPLE_LIST_VIEW = { 'list' : ('list',
                                  MultipleListView,
                                  {})
                    }
FILTERED_LIST_VIEW = { 'list' : ('list/%s' % FILTER_ARGS,
                                  FilteredListView,
                                  {}),
                    }

DETAIL_VIEW = { 'detail': ('detail/%s' % PK_ARG,
                            DetailView,
                            {})
             }

PAGINATED_LIST_VIEW = { 'list' : ('list',
                                   ListView,
                                   lambda action, view, model: { 'paginate_by' : getattr(model,
                                                                                         'PAGINATE_BY',
                                                                                         50) })
}

SEARCH_VIEWS = { 'search' : ('search',
                             SearchView,
                             {})
}

BASE_VIEWS = dict(LIST_VIEW,
                  **EDIT_VIEWS)

EDIT_VIEWS = dict(dict(CREATE_VIEW,
                       **UPDATE_VIEW),
                  **DELETE_VIEW)

FULL_VIEWS = dict(BASE_VIEWS,
                  **DETAIL_VIEW)

