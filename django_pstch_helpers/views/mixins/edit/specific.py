"""
#TODO: Add module docstring
"""
from django.shortcuts import get_object_or_404

from django.db.models.fields.related import ForeignKey

class SpecificCreateMixin(object):
    """
    #TODO: Add class docstring
    """
    template_name_suffix = "create_specific"
    initial_keys = []

    def get_initial(self):
        """
        #TODO: Add method docstring
        """
        initial = super(SpecificCreateMixin, self).get_initial()

        key = self.kwargs.get('specific_key')
        if key in self.initial_keys:
            initial[key] = self.kwargs.get('specific_value')

        return initial

    def get_context_data(self, *args, **kwargs):
        """
        #TODO: Add method docstring
        """
        context = super(SpecificCreateMixin,
                        self).get_context_data(*args, **kwargs)

        key = self.kwargs['specific_key']

        if key in self.initial_keys:
            value = self.kwargs['specific_value']
            field = getattr(self.model, key).field
            context['initial_field'] = key

            if type(field) in [ForeignKey, ]:
                model = field.rel.to
                context['initial_field_model'] = model
                context['initial_value'] = get_object_or_404(model,
                                                             pk=value)
            else:
                context['initial_value'] = value

        return context
