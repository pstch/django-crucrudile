from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from django.db.models.fields.related import ForeignKey, ManyToManyField

from .edit import CreateView

def get_field(model, path):
    keys = path.split('__')
    key = keys.pop(0)
    try:
        if not keys:
            return getattr(model, key)
        else:
            _field = getattr(model, keys.pop(0))
            if type(_field) in [ForeignKey, ]:
                return get_field(_field.rel.to, '__'.join(keys))
            else:
                raise ImproperlyConfigured("Wrong relationship path %s : Field %s is not a ForeignKey" % (path, _field))
    except AttributeError:
        raise ImproperlyConfigured("Wrong relationship path %s :  Could not find field %s in model %s" % (path, key, model))
        
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
        value = self.kwargs['specific_value']

        field = get_field(self.model, key)

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
