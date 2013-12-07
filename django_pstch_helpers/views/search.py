from __future__ import unicode_literals

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from django.shortcuts import render_to_response

from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .mixins import AuthMixin

from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchView(AuthMixin, FormMixin, ListView):
    template_name = 'search/search.html'

    results = EmptySearchQuerySet()

    load_all = True
    searchqueryset = None
    form_class = ModelSearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)

        if len(self.request.GET):
            data = self.request.GET

        results = self.get_results()
            
        context['query'] = self.get_query()
        context['results'] = results

        results_query = getattr(results, 'query', None)
        if results and results_query and results_query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        return context

        
    def get_form_kwargs(self):
        return {'searchqueryset' : self.searchqueryset,
                'load_all' : self.load_all }
        
    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']
        return ''

    def get_queryset(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)
    return search_view


class FacetedSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")

        return super(FacetedSearchView, self).build_form(form_kwargs)

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['request'] = self.request
        extra['facets'] = self.results.facet_counts()
        return extra


def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }

    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))
