from django.contrib import messages

from django.contrib.auth.models import Permission
from django.db.models.deletion import Collector

from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .mixins import AuthMixin, ModelInfoMixin, RedirectMixin

class CreateView(AuthMixin, ModelInfoMixin, RedirectMixin, CreateView):
    def get_template_names(self):
        names = super(CreateView, self).get_template_names()
        names.append("%s/object_create.html" % self.model._meta.app_label)
        names.append("%s/object_form.html" % self.model._meta.app_label)
        return names

    def form_valid(self, form):
        response = super(CreateView, self).form_valid(form)
        messages.success(self.request, "Created object %s (of type %s, of id %s) in the database." % (self.object, self.object.__class__.__name__, self.object.id))
        return response

class UpdateView(AuthMixin, ModelInfoMixin, RedirectMixin, UpdateView):
    def get_template_names(self):
        names = super(UpdateView, self).get_template_names()
        names.append("%s/object_update.html" % self.model._meta.app_label)
        names.append("%s/object_form.html" % self.model._meta.app_label)
        return names

    def form_valid(self, form):
        response = super(UpdateView, self).form_valid(form)
        messages.info(self.request, "Updated object %s (of type %s, of id %s)." % (self.object, self.object.__class__.__name__, self.object.id))
        return response

class DeleteView(AuthMixin, ModelInfoMixin, RedirectMixin, DeleteView):
    def get_template_names(self):
        names = super(DeleteView, self).get_template_names()
        names.append("%s/object_delete.html" % self.model._meta.app_label)
        return names
    def get_context_data(self, *args, **kwargs):
        context = super(DeleteView, self).get_context_data(*args, **kwargs)

        collector = Collector(using='default')
        collector.collect([self.object,])
        
        related = collector.instances_with_model()
        count = related.count()

        if count > 50:
            context['related'] = related[:50]
            context['related_not_shown'] = count - 50
        else:
            context['related'] = related
            
        
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        copy = self.object
        messages.warning(request, "Deleted object %s (of type %s, of id %s) from the database." % (copy, copy.__class__.__name__, copy.id))
        return super(DeleteView, self).delete(request, *args, **kwargs)
