"""
#TODO: Add module docstring
"""
import re
from itertools import chain

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.views.generic import View as View

from django_crucrudile.utils import call_if_needed
from django_crucrudile.views.mixins import ModelActionMixin

def make_model_mixin(view_class,
                     extra_args=None,
                     extra_funcs=None,
                     no_auto_view_mixin=False):
    """Use this function to create a Model action mixin for a given view.

    Arguments :
     -- view : view to use for this mixin.
         (this view should subclass ModelActionMixin)
     -- extra_funcs :
         dict of functions to add on the model mixin.
         (the dict key is the function name, and might be a callable,
          and will be called with view as argument)
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
                    arg_key: call_if_needed(arg_value, cls) \
                    for (arg_key, arg_value) in extra_args.items()
                })
            return args

    @classmethod
    def _get_url(cls):
        return cls.get_url_name(view_class)

    setattr(ModelMixin,
            'get_%s_url' % view_class.get_underscored_action_name(),
            _get_url)

    if extra_funcs:
        for func_name, func in extra_funcs.items():
            func_name = call_if_needed(func_name, view_class)
            setattr(ModelMixin,
                    func_name,
                    func)

    return ModelMixin


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
    def get_url_namespaces(cls):
        """
        #TODO: Add method docstring
        """
        #pylint: disable=R0201

        # FIXME: we have two choices here : we can get app_label from
        # _meta, but it's dirty, or we can get app_label using
        # ContentTypes and get_for_model(cls).app_label. However this
        # introduces a hard dependency to django.contrib.contenttypes
        # not sure yet which one is the best, sticking to _meta to
        # avoid the dependency
        return [cls._meta.app_label, ]

    @classmethod
    def get_url_name(cls, view):
        """
        #TODO: Add method docstring
        """
        action = view.get_action_name()
        name = cls.get_model_name()
        namespaces = cls.get_url_namespaces()

        url_name = '-'.join([name, action]) if name else action
        return ':'.join(namespaces + [url_name,])

    @classmethod
    def get_url_prefix(cls):
        return "/".join(cls.get_url_namespaces)

    @classmethod
    def get_url_patterns_by_view(cls, view):
        url_prefix = cls.get_url_prefix()
        return [url(
            "/".join(
                [url_pefix,] if url_prefix else [] + \
                [url_part] if url_part else []
            ),
            view.as_view(model=cls,
                         **cls.get_args_by_view(view)),
            name=cls.get_url_name(view)
        ) for url_part in view.get_url_parts()]

    @classmethod
    def get_url_patterns(cls):
        urlpatterns = []
        for view in cls.get_views():
            for pattern in cls.get_url_patterns_by_view(view):
                urlpatterns += pattern


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
        auto_patterns(...), to get the nnxeeded views for a Model.

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
        if not view in cls.get_views():
            raise ImproperlyConfigured(
                "Tried to get the view arguments for a view that is not"
                " defined by get_views()"
            )
        return {}
