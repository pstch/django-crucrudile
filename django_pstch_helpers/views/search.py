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


