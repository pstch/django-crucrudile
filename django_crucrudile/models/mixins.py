"""Model mixins utility functions and base classes

Functions :
-- make_model_mixin(view_class, ...): creates a Model
mixin for a given view class, that allows to automatically get URL
patterns from the Model class
-- make_model_mixin([(view_class1), (view_class2)], ...): run the above
function for each tuple given in the list in the first argument. (this tuple
can contain additional parameters to make_model_mixin(...))

Classes :
-- AutoPatternsMixin : base class for model mixins

Tests:
-- ../../tests/test_model_mixins.py
"""
import re
from itertools import chain

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.views.generic import View as View

from django_crucrudile.utils import try_calling
from django_crucrudile.views.mixins import ModelActionMixin

def make_model_mixin(view_class,
                     extra_args=None,
                     extra_funcs=None,
                     no_auto_view_mixin=False):
    """Use this function to create a Model action mixin for a given view.

    Arguments :
    -- view : view to use for this mixin.
         (this view should subclass ModelActionMixin)
    -- extra_args : dict of keyword arguments for the view
    (the dict value is the argument value, and might be a callable,
    and will be called with model as argument)
    -- extra_funcs : dict of functions to add on the model mixin.
    (the dict key is the function name, and might be a callable,
    and will be called with view as argument)
    -- no_auto_view_mixin : disable autopatching of view with ModelActionMixin
    (when view_class is missing a method or attribute from ModelActionMixin,
    it is automatically added (and bound if needed) to view_class. Set this to
    True to disable this behaviour)
    """
    if not no_auto_view_mixin:
        # not inhibiting automatic adding of ModelActionMixin
        # functionality
        for attr in dir(ModelActionMixin):
            if not attr.startswith('__') and \
               not attr.endswith('__') and \
               not hasattr(view_class, attr):
                # we found a non-special attribute in ModeActionMixin
                # that is not present in view_class
                setattr(
                    view_class, attr,
                    ModelActionMixin.__dict__[attr])
                # we use .__dict__[] because we need unbound
                # attributes

    class ModelMixin(AutoPatternsMixin):
        @classmethod
        def get_views(cls):
            views = super(ModelMixin, cls).get_views()
            views.append(view_class)
            return views

        @classmethod
        def get_args_by_view(cls, view):
            args = super(ModelMixin, cls).get_args_by_view(view)
            if view is view_class and extra_args is not None:
                args.update({
                    arg_key: try_calling(arg_value, cls) or arg_value \
                    for (arg_key, arg_value) in extra_args.items()
                })
            return args

    @classmethod
    def _get_url(cls):
        return reverse(cls.get_url_name(view_class))

    setattr(ModelMixin,
            'get_%s_url' % view_class.get_underscored_action_name(),
            _get_url)

    if extra_funcs:
        for func_name, func in extra_funcs.items():
            func_name = try_calling(func_name, view_class) or func_name
            setattr(ModelMixin,
                    func_name,
                    func)

    return ModelMixin

def make_model_mixins(views,
                      no_auto_view_mixin = False):
    """Use this function to create Model action mixinx for the given views

    Return a tuple of model_action_mixins

    Arguments :
    -- views : set of tuples, views to make mixins for (should contain
    tuples (with at least one item and at most three), themselves
    containing :
     - view_class (mandatory)
     - extra_args (optional)
     - extra_func (optional)
    -- no_auto_view_mixin : disable autopatching of view
    with ModelActionMixin (when view_class is missing a method or
    attribute from ModelActionMixin, it is automatically added (and
    bound if needed) to view_class. Set this to True to disable this
    behaviour. See docs fr more information)

    views tuple items :
    -- view : view to use for this mixin.
         (this view should subclass ModelActionMixin)
    -- extra_args : dict of keyword arguments for the view
    (the dict value is the argument value, and might be a callable,
    and will be called with model as argument)
    -- extra_funcs : dict of functions to add on the model mixin.
    (the dict key is the function name, and might be a callable,
    and will be called with view as argument)

    """
    return tuple([
        make_model_mixin(
            *view_tuple,
            no_auto_view_mixin=no_auto_view_mixin
        ) for view_tuple in views
    ])

class AutoPatternsMixin(object):
    """
    Base mixin for all action model mixins
    """
    @classmethod
    def get_model_name(cls):
        """Get the model name
        (example for FooBarTestModel : 'foobartestmodel')
        """
        return cls.__name__.lower()

    @classmethod
    def get_url_name(cls, view):
        """Return the URL name for a given view

        Compiles the URL name using view.get_action_name
        and cls.get_model_name()

        get_model_name() can be None, in which case the URL
        name will be compiled using the action

        """
        action = view.get_action_name()
        name = cls.get_model_name()

        url_name = '-'.join([name, action]) if name else action
        return url_name

    @classmethod
    def get_url_patterns_by_view(cls, view):
        """Get list of URL patterns for a given view"""
        #TODO: Write test
        url_name = cls.get_model_name()

        return [url(
            "/".join(
                filter(None, (url_name, url_part))
            ),
            view.as_view(model=cls,
                         **cls.get_args_by_view(view)),
            name=cls.get_url_name(view)
        ) for url_part in view.get_url_parts()]

    @classmethod
    def get_url_patterns(cls):
        """Get list of URL patterns for all views"""
        #TODO: Write test
        urlpatterns = []
        for view in cls.get_views():
            for pattern in cls.get_url_patterns_by_view(view):
                urlpatterns.append(pattern)
        return urlpatterns


    @classmethod
    def get_views(cls):
        """Return list of views for this model

        This class method is overriden by ModelMixin classes, so that the
        resulting Model object (which subclasses ModelMixin classes)
        can get the list of the views used for this Model with
        get_views().

        When overriden in a ModelMixin class, get_views() should
        always get the current list of views using
        super(...).get_views) before appending a new View.

        This function is used by django-generic-patterns, in
        auto_patterns(...), to get the nnxeeded views for a Model.

        """
        return []

    @classmethod
    def get_args_by_view(cls, view): # pylint: disable=W0613
        """Return dict of keyword arguments for a view

        This class method is overriden by ModelMixin classes, so that the
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
        if not view in cls.get_views():
            raise ImproperlyConfigured(
                "Tried to get the view arguments for a view that is not"
                " defined by get_views()"
            )
        return {}
