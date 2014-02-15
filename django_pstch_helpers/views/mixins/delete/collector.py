from django.views.generic.base import ContextMixin

from django.db.models.deletion import Collector

class DeletionCollectorContextMixin(ContextMixin):
    collector_limit = 50
    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)

        collector = Collector(using='default')
        collector.collect([self.object,])

        related = collector.instances_with_model()
        context['related'] = []
        context['related_not_shown'] = 0

        i = 0
        for model, instance in related:
            if i < self.collector_limit:
                context['related'].append((model, instance))
            else:
                context['related_not_shown'] += 1
            i += 1

        return context
