"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.views import (
    CreateView, SpecificCreateView,
    UpdateView
)

from .base import AutoPatternsMixin

class CreatableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_create_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(CreateView,
                            args=[cls.id,])
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(CreatableModelMixin, cls).get_views()
        views.append(CreateView)
        return views

class SpecificCreatableModelMixin(CreatableModelMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(SpecificCreatableModelMixin, cls).get_views()
        views.append(SpecificCreateView)
        return views
    @classmethod
    def get_args_by_view(cls, view):
        """
        #TODO: Add method docstring
        """
        args = super(SpecificCreatableModelMixin, cls).get_args_by_view(view)
        if view is SpecificCreateView:
            args['initial_keys'] = cls.get_spec_create_init_keys()
        return args
    @staticmethod
    def get_spec_create_init_keys():
        """
        #TODO: Add method docstring
        """
        raise ImproperlyConfigured(
            "get_specific_create_initial_keys should be "
            "overriden to return a proper list of fields"
        )

class UpdatableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_update_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_url(UpdateView,
                            args=[cls.id,])
    @classmethod
    def get_edit_url(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_update_url()
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(UpdatableModelMixin, cls).get_views()
        views.append(UpdateView)
        return views
