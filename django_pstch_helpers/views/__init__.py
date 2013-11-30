from django.shortcuts import render
from django.contrib import messages

from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic import TemplateView as HaystackSearchView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin


class TemplateView(AuthMixin, TemplateView):
    pass

class ListView(AuthMixin, ModelInfoMixin, ListView):
    select_related = None
    prefetch_related = None
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                manager = queryset
        elif self.model is not None:
            manager = self.model._default_manager
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        if self.select_related is not None:
            queryset = manager.select_related(*self.select_related).all()
        else:
            queryset = manager.all()
            
        return queryset
                                                                                                                                                                )
    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_list.html" % self.model._meta.app_label)
        return names

class DetailView(AuthMixin, ModelInfoMixin, DetailView):
    def get_template_names(self):
        names = super(DetailView, self).get_template_names()
        names.append("%s/object_detail.html" % self.model._meta.app_label)
        return names

class HomeView(TemplateView):
    pass


class SearchView(AuthMixin, HaystackSearchView):
    pass
