"""
#TODO: Add module docstring
"""
from django_pstch_helpers.utils import contribute_viewset_to_views

from django_pstch_helpers.sets import DetailViewSet
from .base import AutoPatternsMixin

class DetailableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    def get_detail_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_url(DetailViewSet.action,
                            args=[self.id,])
    def get_absolute_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_detail_url()
    def get_views(self):
        """
        #TODO: Add method docstring
        """
        views = super(DetailableModelMixin, self).get_views()
        contribute_viewset_to_views(views, DetailViewSet)
        return views
