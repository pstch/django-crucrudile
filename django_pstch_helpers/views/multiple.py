from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, ContextMixin

from . import View
from .mixins import AuthMixin, ModelInfoMixin

class MultipleModelMultipleObjectMixin(ContextMixin):
    """
    A mixin for views manipulating multiple objects from multiple models
    (no support for pagination)
    (to use pagination in such a setup, it would be more practical to use AJAX requests)
    """
    allow_empty = True
    querysets = None
    models = None

    def get_querysets(self):
        """
        Return the list of items for this view.

        The return value must be a list (iterable) of querysets. By queryset, 
        I mean any iterable that may be an instance of `QuerySet`,
        in which case `QuerySet` specific behavior will be enabled.
        """
        if self.querysets is not None:
            for model, queryset in self.querysets.items():
                if isinstance(queryset, QuerySet):
                    self.querysets[model] = queryset.all()
                querysets = self.querysets
        elif self.models is not None:
            querysets = {}
            for model in self.models:
                querysets[model] = model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing its QuerySets. Define "
                "%(cls)s.models, %(cls)s.querysets, or override "
                "%(cls)s.get_querysets()." % {
                    'cls': self.__class__.__name__
                }
            )
        return querysets

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        querysets = kwargs.pop('object_lists', self.object_lists)
        context = {}
        
        for model, queryset in querysets.items():
            model = model._meta.module_name
            context['%s_list' % model] = queryset

        context['querysets'] = querysets

        context.update(kwargs)
        return super(MultipleModelMultipleObjectMixin, self).get_context_data(**context)


class BaseMultipleListView(MultipleModelMultipleObjectMixin, View):
    """
    A base view for displaying a list of objects from different models.
    """
    def get(self, request, *args, **kwargs):
        self.object_lists = self.get_querysets()
        context = self.get_context_data()
        return self.render_to_response(context)


class MultipleModelMultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for responding with a template and list of objects.
    """
    template_name_suffix = '_lists'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        try:
            names = super(MultipleModelMultipleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        model_names = []
        app_label = ""

        for model in self.object_lists:
            if not app_label:
                app_label = model._meta.app_label
            else:
                if not app_label == model._meta.app_label:
                    raise ImproperlyConfigured("Diverging app_labels in the specified models")

            model_names.append(model._meta.module_name)
        model_names.sort()
        model_names = '+'.join(model_names)
        names.append("%s/%s%s.html" % (app_label, model_names, self.template_name_suffix))

        return names

class MultipleListView(AuthMixin, MultipleModelMultipleObjectTemplateResponseMixin, ModelInfoMixin, BaseMultipleListView):
    """
    Render some lists of objects, set by `self.models` or `self.querysets`.
    `self.queryset` can actually be any list of iterables of items, not just a list of querysets.
    """
