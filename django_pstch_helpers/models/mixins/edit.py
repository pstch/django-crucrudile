"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured

from django_pstch_helpers.views import (
    CreateView, SpecificCreateView,
    UpdateView,
    DeleteView
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

class SpecificCreatableModelMixin(AutoPatternsMixin):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_specific_create_url(cls):
        """
        #TODO: Add method docstring
        """
        #TODO: Missing args, reverse won't work
        return cls.get_url(SpecificCreateView,
                            args=[cls.id,])
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
    @classmethod
    def get_spec_create_init_keys(cls):
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
    def get_update_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_url(UpdateView,
                            args=[self.id,])
    def get_edit_url(self):
        """
        #TODO: Add method docstring
        """
        return self.get_update_url()
    @classmethod
    def get_views(cls):
        """
        #TODO: Add method docstring
        """
        views = super(UpdatableModelMixin, cls).get_views()
        views.append(UpdateView)
        return views

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
