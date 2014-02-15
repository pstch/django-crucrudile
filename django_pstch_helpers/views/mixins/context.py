from django.views.generic.base import ContextMixin

class ExtraContextMixin(ContextMixin):
    """
    This mixin will read extra_context when get_context_data is called, and update the context with its contents.

    If extra_context or one of its values is a callable, it will be called in get_context_data with the view and current context as arguments.
    """
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        if callable(self.extra_context):
            extra_context = self.extra_context(self, context)
        else:
            extra_context = self.extra_context

        for key in extra_context:
            if callable(extra_context[key]):
                extra_context[key] = extra_context[key](self, context)

        context.update(extra_context)

        return context

class ModelInfoMixin(ContextMixin):
    """
    Adds the current model(s) to the template context

    Gets the current model from :
        self.model or self.queryset.model

    Gets the current models from :
        self.models or queryset.model for each queryset in self.querysets
    """
    def get_context_data(self, **kwargs):
        context = super(ModelInfoMixin, self).get_context_data(**kwargs)

        if hasattr(self, 'model'):
            context['model'] = self.model
        elif hasattr(self, 'queryset'):
            if hasattr(self.queryset, 'model'):
                context['model'] = self.queryset.model

        if hasattr(self, 'models'):
            context['models'] = self.model
        elif hasattr(self, 'querysets'):
            # we use list(set(...)) to remove duplicate models
            context['models'] = list(set([queryset.model for queryset in self.querysets]))

        return context
