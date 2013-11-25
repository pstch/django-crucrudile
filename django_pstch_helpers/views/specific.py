from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from .edit import CreateView

class SpecificCreateView(CreateView):
    initial_keys = []
    def get_initial(self):
        
        initial = super(SpecificCreateView, self).get_initial()
        print self.kwargs
        if self.kwargs.get('specific_key') in self.initial_keys:
            print "HAHAHAHA"
            initial[self.kwargs.get('specific_key')] = self.kwargs.get('specific_value')
            print initial
        else:
            print "BUH"
            print self.initial_keys

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(SpecificCreateView, self).get_context_data(*args, **kwargs)

        field = getattr(self.model, self.kwargs['specific_key']).field

        context['specific_key_str'] = context['specific_key']

        if type(field) in [ForeignKey, ManyToManyField]:

            context['specific_key'] = field.rel.to

            context['specific_value'] = get_object_or_404(context['specific_key'],
                                                        pk = self.kwargs['specific_value'])
        else:
            context['specific_key'] = self.kwargs['specific_key']
            context['specific_value'] = self.kwargs['specific_value']

        return context

    def get_template_names(self):
        names = super(SpecificCreateView, self).get_template_names()
        names.append("%s/object_create_specific.html" % self.model._meta.app_label)
        names.append("%s/%s_create_specific.html" % (self.model._meta.app_label,
                                                     self.model._meta.model_name))

        return names
