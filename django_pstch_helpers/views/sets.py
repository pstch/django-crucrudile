from .utils import mix_views

from . import ListView, DetailView, SearchView
from .multiple import MultipleListView
from .edit import CreateView, DeleteView, UpdateView 
from .filtered import FilteredListView
from .specific import SpecificCreateView

PK_ARG = "(?P<pk>\d+)"
FILTER_ARGS = "of-(?P<filter_key>\w+)/(?P<filter_value>\d+)"
SPECIFIC_ARGS = "of-(?P<specific_key>\w+)/(?P<specific_value>\d+)"


CREATE_VIEW = { 'create' : ('create$',
                           CreateView,
                           {})}

SPECIFIC_CREATE_VIEW = { 'create' : ('create/%s$' % SPECIFIC_ARGS,
                         SpecificCreateView,
                         {}),}

UPDATE_VIEW =  { 'update' : ('update/%s' % PK_ARG,
                             UpdateView,

                             {}),}
DELETE_VIEW = { 'delete' : ('delete/%s' % PK_ARG,
                           DeleteView,
                           {}),}

LIST_VIEW = { 'list' : ('list$',
                         ListView,
                         {})
           }

MULTIPLE_LIST_VIEW = { 'list' : ('list$',
                                  MultipleListView,
                                  {})
                    }
FILTERED_LIST_VIEW = { 'filtered-list' : ('list/%s$' % FILTER_ARGS,
                                          FilteredListView,
                                  {}),
                    }

DETAIL_VIEW = { 'detail': ('detail/%s$' % PK_ARG,
                            DetailView,
                            {})
             }

PAGINATED_LIST_VIEW = { 'list' : ('list$',
                                   ListView,
                                   lambda action, view, model: { 'paginate_by' : getattr(model,
                                                                                         'PAGINATE_BY',
                                                                                         50) })
}

SEARCH_VIEWS = { 'search' : ('search',
                             SearchView,
                             {})
}

FORM_VIEWS = mix_views(CREATE_VIEW,
                       UPDATE_VIEW)

EDIT_VIEWS = mix_views(FORM_VIEWS,
                    FORM_VIEWSUPDATE_VIEW,
                       DELETE_VIEW)

BASE_VIEWS = mix_views(EDIT_VIEWS,
                       LIST_VIEW)

FULL_VIEWS = mix_views(BASE_VIEWS,
                       DETAIL_VIEW)
