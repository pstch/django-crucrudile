from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from . import ListView

class FilteredListView(ListView):
    filter_keys = []
    def get_queryset(self, filter = True):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        filter_dict = {}

        if not self.kwargs['filter_key'] in self.filter_keys:
            raise ImproperlyConfigured(
                "%s is not present in filter_keys (%s)" % (self.kwargs['filter_key'], self.filter_keys)
            )

        if filter:
            filter_dict = { self.kwargs['filter_key'] : self.kwargs['filter_value'] }

        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(**filter_dict)
        elif self.model is not None:
            queryset = self.model._default_manager.filter(**filter_dict)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(FilteredListView, self).get_context_data(*args, **kwargs)
        model = getattr(self.model,self.kwargs['filter_key']).field.rel.to
        instance = get_object_or_404(model, pk = self.kwargs['filter_value'])

        for key in self.filter_keys:
            context['%s_list' % key] = getattr(self.model,key).field.rel.to.objects.all()
        
        context['filter_key'] = model
        context['filter_value'] = instance

        context['unfiltered_count'] = self.get_queryset(filter = False).count()

        return context


    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_list_filtered.html" % self.model._meta.app_label)
        return names

