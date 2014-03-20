"""
#TODO: Add module docstring
"""
from django_pstch_helpers.views import DetailView

from .base import AutoPatternsMixin

class DetailableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_detail_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(DetailView,
                            args=[cls.id,])
    @classmethod
    def get_absolute_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_detail_url()
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(DetailableModelMixin, cls).get_views()
        views.append(DetailView)
        return views
