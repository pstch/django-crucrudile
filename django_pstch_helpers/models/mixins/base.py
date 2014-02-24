"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from django_pstch_helpers.utils import make_url_name

class ModelInfoMixin(object):
    """
    #TODO: Add class docstring
    """
    #TODO: Write tests for this class :
    # with a sample Model where we test each function
    @classmethod
    def _get_objects(cls):
        """
        #TODO: Add method docstring
        """
        try:
            objects = cls.objects
            return objects
        except AttributeError:
            raise ImproperlyConfigured(
                "Could not find manager : 'objects' not present on"
                " the current object. Check that ModelInfoMixin is"
                " used on a Model object (currently %s)." % \
                cls.__class__.__name__)

    @classmethod
    def _get_meta(cls):
        """
        #TODO: Add method docstring
        """
        try:
            _meta = cls._meta
            return _meta
        except AttributeError:
            raise ImproperlyConfigured(
                "Could not find manager : '_meta' not present on"
                " the current object. Check that ModelInfoMixin is"
                " used on a Model object (currently %s)." % \
                cls.__class__.__name__)

    @classmethod
    def get_verbose_name(cls):
        """
        #TODO: Add method docstring
        """
        _meta = cls._get_meta()
        return _meta.verbose_name
    @classmethod
    def get_count(cls):
        """
        #TODO: Add method docstring
        """
        objects = cls._get_objects()
        return objects.count()
    @classmethod
    def get_model_name(cls):
        """
        #TODO: Add method docstring
        """
        _meta = cls._get_meta()
        return _meta.model_name

class AutoPatternsMixin(ModelInfoMixin):
    """
    #TODO: Add class docstring
    """
    #TODO: Write tests for this class :
    # with a sample Model where we test each function
    @classmethod
    def get_url_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_model_name()
    @classmethod
    def get_url_prefix(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        return None
    @classmethod
    def get_views(cls):
        """
        Base get_views() function, must be here for the MRO. Returns a
        dictionary containing the views defined by each ModelMixin.

        Each ModelMixin should override this function and
        use contribute_viewset_to_views to add the data
        from its ViewSet.

        Usually called with super(..., self).get_views()
        """
        #pylint: disable=R0201
        return {}
    @classmethod
    def get_view_args(cls):
        """
        Similar to get_views(), but here we don't use a function like
        contribute_viewset_to_views. Returns a dictionary containing
        the view arguments defined by each ModelMixin and by the Model
        classes. Each value should also be a dictionary, with key the
        action name and as a value the keyword arguments to pass to
        the view.
        """
        #pylint: disable=R0201
        return {}
    @classmethod
    def get_url_namespaces(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        return []
    @classmethod
    def _make_url_name(cls, action):
        """
        #TODO: Add method docstring
        """
        return make_url_name(cls.get_url_namespaces(),
                             cls.get_url_name(),
                             action)
    @classmethod
    def get_url(cls, action, args=None):
        """
        #TODO: Add method docstring
        """
        return reverse(cls._make_url_name(action),
                           args=args)

