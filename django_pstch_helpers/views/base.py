from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View, TemplateView, ListView, DetailView

from sortable_listview import SortableListView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin, SelectRelatedMixin

class TemplateView(AuthMixin, TemplateView):
    pass

class ListView(AuthMixin, ModelInfoMixin, SortableListView, SelectRelatedMixin):
    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_%s.html" % (self.model._meta.app_label, self.template_name_suffix))
        return names

class DetailView(AuthMixin, ModelInfoMixin, DetailView):
    def get_template_names(self):
        names = super(DetailView, self).get_template_names()
        names.append("%s/object_%s.html" % (self.model._meta.app_label, self.template_name_suffix))
        return names

class HomeView(TemplateView):
    pass

