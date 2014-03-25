"""
#TODO: Add module docstring
"""
import re

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.views.generic import View as DjangoView

from django_pstch_helpers.utils import make_url_name
from django_pstch_helpers.views import View

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
    @classmethod
    def get_dashed_verbose_name(cls):
        """
        #TODO: Add method docstring
        """
        step = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', step).lower()

class AutoPatternsMixin(ModelInfoMixin):
    """
    #TODO: Add class docstring
    """
    #TODO: Write tests for this class :
    # with a sample Model where we test each function
    @classmethod
    def get_url_prefix(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        return None
    @classmethod
    def get_url_namespaces(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201
        return [cls._meta.app_label, ]
    @classmethod
    def get_url_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_dashed_verbose_name()
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
        if type(action) is str:
            return reverse(cls._make_url_name(action),
                           args=args)
        elif isinstance(action, type):
            if issubclass(action, View) or \
               issubclass(action, DjangoView):
                if hasattr(action, 'get_action_name'):
                    url_name = cls._make_url_name(
                        action.get_action_name()
                    )
                    return reverse(url_name, args=args)
                else:
                    raise ImproperlyConfigured(
                        "action was a view, but it did not define "
                        "get_action_name. get_url needs a valid definition of "
                        "the classmethod/staticmethod get_action_name, that "
                        "should return a string for the action, such a 'list'"
                    )
        else:
            raise TypeError(
                "Unknown type for the 'action' kwarg, neither a string nor a View"
            )

    @classmethod
    def get_views(cls):
        """This class method is overriden by ModelMixin classes, so that the
        resulting Model object (which subclasses ModelMixin classes)
        can get the list of the views used for this Model with
        get_views().

        When overriden in a ModelMixin class, get_views() should
        always get the current list of views using
        super(...).get_views) before appending a new View.

        This function is used by django-generic-patterns, in
        auto_patterns(...), to get the needed views for a Model.

        """
        return []

    @classmethod
    def get_args_by_view(cls, view): # pylint: disable=W0613
        """This class method is overriden by ModelMixin classes, so that the
        resulting Model object (which subclasses ModelMixin classes)
        can get the dictionary of view arguments for each view used in
        this Model, with get_args_by_view(view).

        When overriden in a ModelMixin class or by the user,
        get_args_by_view should always get the current list of views
        using super(...).get_views) before appending a new
        View. Usually, args are tretrieved using super, then if the
        'view' kwarg is the view on which we want to set arguments, we
        update the args dictionary with another dictionary.

        This function is used by django-generic-patterns, in
        auto_patterns(...), to get the needed views for a Model.
        """
        return {}
