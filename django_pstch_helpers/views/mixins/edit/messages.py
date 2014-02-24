"""
#TODO: Add module docstring
"""
#pylint: disable=R0903
from django.contrib import messages

class CreateMessageMixin(object):
    """
    #TODO: Add class docstring
    """
    def form_valid(self, form):
        """
        #TODO: Add method docstring
        """
        response = super(CreateMessageMixin, self).form_valid(form)
        message = "Created object %s (of type %s, of id %s) in the database." \
                  % (self.object,
                     self.object.__class__.__name__,
                     self.object.id)
        messages.success(self.request,
                         message)
        return response

class UpdateMessageMixin(object):
    """
    #TODO: Add method docstring
    """
    def form_valid(self, form):
        """
        #TODO: Add method docstring
        """
        response = super(UpdateMessageMixin, self).form_valid(form)
        message = "Updated object %s (of type %s, of id %s)." \
                   % (self.object,
                      self.object.__class__.__name__,
                      self.object.id)
        messages.info(self.request,
                      message)
        return response

