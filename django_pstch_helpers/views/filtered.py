from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from . import ListView

class FilteredListView(ListView):
    filter_model = None
    filter_attribute = None
    filter_instance = None

    def get_filter_model(self):
        """
        Return the model class specified by filter_key

        """
        if not self.filter_model:
            self.filter_model = get_object_or_404(ContentType, name = self.kwargs['filter_key']).model_class()
        return self.filter_model()

    def get_filter_instance(self):
        """
        Return the instance of the filter model specified by filter_value

        """
        if not self.filter_instance:
            self.filter_instance = get_object_or_404(self.get_filter_model(),
                                                     pk = self.kwargs['filter_value'])
        return self.filter_instance()
        
    def get_django_filter_dict(self):
        return { self.kwargs['filter_key'] if not self.filter_attribute else self.filter_attribute : self.get_filter_instance() }

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        filter = self.get_django_filter_dict()

        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.filter(*filter)
        elif self.model is not None:
            queryset = self.model._default_manager.filter(*filter)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset
