from django.core.exceptions import ImproperlyConfigured
from django.views.generic.list import MultipleObjectMixin

class SelectRelatedMixin(MultipleObjectMixin):
    select_related = None
    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        try:
            manager = self.queryset or self.model._default_manager
        except AttributeError:
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
