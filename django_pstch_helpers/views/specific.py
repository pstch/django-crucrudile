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

    def get_template_names(self):
        names = super(ListView, self).get_template_names()
        names.append("%s/object_create_specific.html" % self.model._meta.app_label)
        return names
