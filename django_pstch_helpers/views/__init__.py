from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View as DjangoView, TemplateView as DjangoTemplateView, DetailView as DjangoDetailView, ListView as DjangoListView
#from haystack.views import SearchView as HaystackSearchView
from django.views.generic import ListView as HaystackSearchView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin

class View(DjangoView):
    pass

class TemplateView(AuthMixin, DjangoTemplateView):
    pass

class ListView(AuthMixin, ModelInfoMixin, DjangoListView):
    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_list.html" % self.model._meta.app_label)
        return names

class DetailView(AuthMixin, ModelInfoMixin, DjangoDetailView):
    def get_template_names(self):
        names = super(DetailView, self).get_template_names()
        names.append("%s/object_detail.html" % self.model._meta.app_label)
        return names

class HomeView(AuthMixin, DjangoTemplateView):
    pass

class SearchView(AuthMixin, HaystackSearchView):
    pass
