from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from .edit import CreateView

class SpecificCreateView(CreateView):
    initial_keys = []
    def get_initial(self):
        initial = super(SpecificCreateView, self).get_initial()

        if self.kwargs.get('specific_key') in self.initial_keys:
            initial[self.kwargs.get('specific_key')] = self.kwargs.get('specific_value')

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(SpecificCreateView, self).get_context_data(*args, **kwargs)

        key = self.kwargs['specific_key']
        
        if key in self.initial_keys:
            value = self.kwargs['specific_value']
            field = getattr(self.model, key)
            context['initial_field'] = key

            if type(field) in [ForeignKey, ]:
                model = field.rel.to
                context['initial_field_model'] = model
                context['initial_value'] = get_object_or_404(model,
                                                             pk = value)
            else:
                context['initial_value'] = value

        return context

    def get_template_names(self):
        names = super(SpecificCreateView, self).get_template_names()
        names.append("%s/object_create_specific.html" % self.model._meta.app_label)
        names.append("%s/%s_create_specific.html" % (self.model._meta.app_label,
                                                     self.model._meta.model_name))

        return names
