from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from . import ListView

class FilteredListView(ListView):
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        filter = { "%s__pk" % self.kwargs['filter_key'] : self.kwargs['filter_value'] }

        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(**filter)
        elif self.model is not None:
            queryset = self.model._default_manager.filter(**filter)
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
        model = getattr(self.model,
                        self.kwargs['filter_key']).field.rel.to
        instance = get_object_or_404(model, pk = self.kwargs['filter_value'])
        
        context['filter_key'] = model
        context['filter_value'] = instance

        return context
