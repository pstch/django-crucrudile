from django.views.generic.edit import FormMixin

from django.contrib import messages

class CreateMessageMixin(FormMixin):
    def form_valid(self, form):
        response = super(CreateView, self).form_valid(form)
        messages.success(self.request, "Created object %s (of type %s, of id %s) in the database." % (self.object, self.object.__class__.__name__, self.object.id))
        return response

class UpdateMessageMixin(FormMixin):
    def form_valid(self, form):
        response = super(UpdateView, self).form_valid(form)
        messages.info(self.request, "Updated object %s (of type %s, of id %s)." % (self.object, self.object.__class__.__name__, self.object.id))
        return response

