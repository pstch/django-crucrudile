"""
#TODO: Add module docstring
"""
from django_pstch_helpers.views import DetailView

from .base import AutoPatternsMixin

class DetailableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    def get_detail_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_url(DetailView,
                            args=[self.id,])
    def get_absolute_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_detail_url()
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(DetailableModelMixin, cls).get_views()
        views.append(DetailView)
        return views
