from django.views.generic.edit import DeletionMixin
from django.contrib import messages

class DeleteMessageMixin(DeletionMixin):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        copy = self.object
        messages.warning(request, "Deleted object %s (of type %s, of id %s) from the database." % (copy, copy.__class__.__name__, copy.id))
        return super(DeleteView, self).delete(request, *args, **kwargs)
