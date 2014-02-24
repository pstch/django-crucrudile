"""
#TODO: Add module docstring
"""
from django.views.generic.edit import DeletionMixin
from django.contrib import messages

class DeleteMessageMixin(DeletionMixin):
    """
    #TODO: Add class docstring
    """
    def delete(self, request, *args, **kwargs):
        """
        #TODO: Add method docstring
        """
        self.object = self.get_object()
        copy = self.object
        messages.warning(request,
                         "Deleted object %s (of type %s, of id %s)"
                         " from the database." %\
                         (copy, copy.__class__.__name__, copy.id))
        return super(DeleteMessageMixin, self).delete(request, *args, **kwargs)
