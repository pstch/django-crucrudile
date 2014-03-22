"""
#TODO: Fix module docstring
"""
#pylint: disable=R0903

from django.core.exceptions import ImproperlyConfigured


class ExtraContextMixin(object): #TODO: test inheriting from ContextMixin
    """
    This mixin will read extra_context when get_context_data is
    called, and update the context with its contents.

    If extra_context or one of its values is a callable, it will be
    called in get_context_data with the view and current context as
    arguments.
    """
    extra_context = {}
    def get_context_data(self, **kwargs):
        """
        Adds extra_context to the template context, replacing
        callables (and callables dict values) with their return value
        if there are any.
        """
        super_object = super(ExtraContextMixin, self)
        if hasattr(super_object, 'get_context_data'):
            context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        else:
            context = {}

        if callable(self.extra_context):
            #pylint: disable=E1102
            extra_context = self.extra_context(self, context.copy())
        else:
            extra_context = self.extra_context

        for key in extra_context:
            if callable(extra_context[key]):
                extra_context[key] = extra_context[key](self, context.copy())

        context.update(extra_context)

        return context

class ModelInfoMixin(object):
    """
    Adds the current model(s) to the template context

    Gets the current model from :
        self.model or self.queryset.model

    Gets the current models from :
        self.models or queryset.model for each queryset in self.querysets
    """
    def get_context_data(self, **kwargs):
        """
        Adds to the template context :
         -- model view attribute to the template context.
        (if model is not defined, we try to use the queryset attribute)
         -- models view attribute to the template context.
        (f models is not defined, we try to use the querysets attrbute.)
        """
        context = super(ModelInfoMixin, self).get_context_data(**kwargs)

        if hasattr(self, 'model'):
            context['model'] = self.model
        elif hasattr(self, 'queryset'):
            if hasattr(self.queryset, 'model'):
                context['model'] = self.queryset.model

        if hasattr(self, 'models'):
            context['models'] = self.models
        elif hasattr(self, 'querysets'):
            # we use list(set(...)) to remove duplicate models
            context['models'] = list(
                set([queryset.model for queryset in self.querysets])
            )
        if not context.get('model') and \
           not context.get('models'):
            raise ImproperlyConfigured(
                """%(cls)s uses the ModelInfoMixin, and could not find
                the current (or list of) models. Please check that the
                model/models attribute is defined, or that the
                queryset attribute value has a model attribute, or
                that the querysets attribute contains a list of
                objects with a model attribute.
                """ % {'cls' : self.__class__.__name__}
            )

        return context
