from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View as View, TemplateView, ListView, DetailView
from django.views.generic import TemplateView as HaystackSearchView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin

class View(AuthMixin, View):
    pass

class TemplateView(AuthMixin, TemplateView):
    pass

class ListView(View, ModelInfoMixin, ListView):
    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_list.html" % self.model._meta.app_label)
        return names

class DetailView(View, ModelInfoMixin, DetailView):
    def get_template_names(self):
        names = super(DetailView, self).get_template_names()
        names.append("%s/object_detail.html" % self.model._meta.app_label)
        return names

class HomeView(View,TemplateView):
    pass

class SearchView(View, HaystackSearchView):
    pass
