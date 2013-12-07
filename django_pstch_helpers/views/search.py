from __future__ import unicode_literals

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from django.shortcuts import render_to_response

from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from .mixins import AuthMixin

from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchView(AuthMixin, MultipleObjectMixin, FormMixin, TemplateView):
    template_name = 'search/search.html'

    queryset = EmptySearchQuerySet()
    query = ''
    
    load_all = True
    searchqueryset = None
    form_class = ModelSearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)

        if len(self.request.GET):
            data = self.request.GET

        context['query'] = self.query

        results = self.queryset
        results_query = getattr(results, 'query', None)
        if results and results_query and results_query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        return context

        
    def get_form_kwargs(self):
        return {'searchqueryset' : self.searchqueryset,
                'load_all' : self.load_all }

    def form_valid(self, form):
        self.query = form.cleaned_data['q']
        self.queryset = form.search()
        return super(SearchView, self).form_valid(form)
        

