from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic import TemplateView as HaystackSearchView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin

class TemplateView(AuthMixin, TemplateView):
    pass

class ListView(AuthMixin, ModelInfoMixin, ListView):
    select_related = []
    prefetch_related = []
#    def get_template_names(self):
#        names = super(ListView, self).get_template_names()
#        names.append("%s/object_list.html" % self.model._meta.app_label)
#        return names

class DetailView(AuthMixin, ModelInfoMixin, DetailView):
    pass
#    def get_template_names(self):
#        names = super(DetailView, self).get_template_names()
#        names.append("%s/object_detail.html" % self.model._meta.app_label)
#        return names

class HomeView(AuthMixin, TemplateView):
    pass

class SearchView(AuthMixin, HaystackSearchView):
    pass
