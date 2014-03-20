"""
#TODO: Add module docstring
"""
from django_pstch_helpers.views import DeleteView

from .base import AutoPatternsMixin

class DeletableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_delete_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(DeleteView,
                            args=[cls.id,])
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(DeletableModelMixin, cls).get_views()
        views.append(DeleteView)
        return views
