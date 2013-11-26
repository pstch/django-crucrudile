from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from . import ListView

class FilteredListView(ListView):
    filter_keys = []
    def get_queryset(self, filter = True):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        key = self.kwargs['filter_key']
        value = self.kwargs['filter_value']

        filter_dict = {}

        if not key in self.filter_keys:
            raise ImproperlyConfigured(
                "%s is not present in filter_keys (%s)" % (key, self.filter_keys)
            )

        key = "__".join(key.split("."))

        if filter:
            filter_dict = { key : value }

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
        def get_field(model,keys):

            labels = []

            sub_attr = getattr(model, keys[0])
            sub_field = sub_attr.field
            sub_model = sub_field.rel.to

            if len(keys) is 1:
                if type(sub_field) in [ForeignKey, ManyToManyField]:
                    labels.append(sub_model._meta.verbose_name)
                else:
                    labels.append(keys[0])
                return sub_field, labels

            labels.append(sub_model._meta.verbose_name)
            field, _labels = get_field(sub_model, keys[1:])
            labels += _labels
            return field, labels

        context = super(FilteredListView, self).get_context_data(*args, **kwargs)

        key = self.kwargs['filter_key']
        value = self.kwargs['filter_value']
        
        field, labels = get_field(self.model, key.split("__")) 
        context['filter_key_labels'] =  labels

        if type(field) in [ForeignKey,ManyToManyField]:
            field_target = field.rel.to

            context['filter_key'] = field_target

            context['filter_value'] = get_object_or_404(field_target,
                                                        pk = value)
        else:

            context['filter_key'] = key
            context['filter_value'] = value


        context['filter_list'] = {}
        for key in self.filter_keys:
            labels, field = get_field(self.model, key.split("__"))
            if type(field) in (ForeignKey, ManyToManyField):
                if not field.rel.to is self.model:
                    context['filter_list'][str(key)] = { 'labels' : labels,
                                                         'list' : getattr(self.model,key).field.rel.to.objects.all() }
        
        context['unfiltered_count'] = self.get_queryset(filter = False).count()

        return context


    def get_template_names(self):
        names = super(FilteredListView, self).get_template_names()
        names.append("%s/%s_list_filtered.html" % (self.model._meta.app_label,
                                                     self.model._meta.model_name))
        names.append("%s/object_list_filtered.html" % self.model._meta.app_label)
        return names

