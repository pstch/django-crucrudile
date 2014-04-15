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
#pylint: disable=W0141, W0142
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf.urls import url

from django_crucrudile.utils import try_calling, monkeypatch_mixin
from django_crucrudile.views.mixins import ModelActionMixin

def make_model_mixin(view_class,
                     extra_args=None,
                     extra_funcs=None,
                     no_auto_view_mixin=False):
    """Use this function to create a Model action mixin for a given view.

    Arguments :
    -- view : view to use for this mixin
    (this view should subclass ModelActionMixin)
    -- extra_args : dict of keyword arguments for the view (the dict
    value is the argument value, and might be a callable, and will be
    called with model as argument)
    -- extra_funcs : dict of functions to add on the model mixin.
    (the dict key is the function name, and might be a callable, and
    will be called with view as argument)
    -- no_auto_view_mixin : disable autopatching of view with ModelActionMixin
    (when view_class is missing a method or attribute from ModelActionMixin,
    it is automatically added (and bound if needed) to view_class. Set this to
    True to disable this behaviour)
    """
    if not no_auto_view_mixin:
        # not inhibiting automatic adding of ModelActionMixin
        # functionality
        view_class = monkeypatch_mixin(view_class, ModelActionMixin)

    class ModelMixin(AutoPatternsMixin):
        """Class mixin created by make_model_mixin, in order to dynamically
        define the needed functions based on the arguments.

        """
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
    def _get_url(cls, *args, **kwargs):
        """Private function, renamed to get_<action>_url when monkeypatched to
        the view. Used to implement model functions such as
        get_list_url()

        """
        return reverse(
            cls.get_url_name(view_class, prefix=True),
            *args,
            **kwargs
        )

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
                      no_auto_view_mixin=False):
    """Use this function to create Model action mixinx for the given views

    Return a tuple of model_action_mixins

    Arguments :
    -- views : set of tuples, views to make mixins for (should contain
    tuples (with at least one item and at most three), themselves
    containing :
     - view_class (mandatory)
     - extra_args (optional)
     - extra_func (optional)
    -- no_auto_view_mixin : disable autopatching of view with
    ModelActionMixin (when view_class is missing a method or attribute
    from ModelActionMixin, it is automatically added (and bound if
    needed) to view_class. Set this to True to disable this
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
    url_namespaces = []
    @classmethod
    def get_model_name(cls):
        """Get the model name
        (example for FooBarTestModel : 'foobartestmodel')
        """
        return cls.__name__.lower()

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
        """
        if not view in cls.get_views():
            raise ImproperlyConfigured(
                "Tried to get the view arguments for a view that is not"
                " defined by get_views()"
            )
        return {}

    @classmethod
    def get_url_namespaces(cls, no_content_types=False):
        """Returns the list of URL namespaces to use when creating the URLs.

        To disable usage of URL namespaces, set this to return an
        empty list.  You will need to override this if don't want the
        application name as a namespace.

        """
        if not cls.url_namespaces:
            try:
                if no_content_types is True: # force fallback to _meta.app_label
                    raise ImportError(
                        "django.contrib.contenttypes import explicitly disabled"
                    )
                from django.contrib.contenttypes.models import ContentType
            except ImportError:
                cls.url_namespaces = [cls._meta.app_label, ]
            else:
                cls.url_namespaces = [
                    ContentType.objects.get_for_model(cls).app_label,
                ]
        return cls.url_namespaces

    @classmethod
    def get_url_name(cls, view, prefix=False):
        """Return the URL name for a given view

        Compiles the URL name using view.get_action_name() and
        cls.get_model_name() (and namespaces kwarg if specified)

        get_model_name() can be None, in which case the URL
        name will be compiled using the action

        """
        name = '-'.join(filter(
            None,
            [cls.get_model_name(),
             view.get_action_name()]
        ))

        namespaces_list = cls.get_url_namespaces()
        if prefix and namespaces_list:
            return ':'.join(cls.get_url_namespaces() + [name, ])
        return name

    @classmethod
    def get_url_prefix(cls):
        """Return path prefix

        By default, returns an empty string (so that the URL is
        prefixed directly in urls.py), but it's possible to return a
        prefix based on get_url_namespaces() too.

        """
        return None

    @classmethod
    def get_url_patterns_by_view(cls, view):
        """Get list of URL patterns for a given view and its URL parts
(combinations of URL arguments specification)"""

        def make_url(url_part):
            """Make URL pattern (join prefix, model name, and view's URL part)

            """
            return '/'.join(filter(
                None,
                [
                    cls.get_url_prefix(),
                    cls.get_model_name(),
                    url_part
                ]
            ))
        def make_view():
            """Create view callback using current model and args from
            get_args_by_view"""
            return view.as_view(
                model=cls,
                **cls.get_args_by_view(view)
            )
        def make_name():
            """View URL name (unprefixed, this is the name we give to url())"""
            return cls.get_url_name(view)

        return [
            url(
                make_url(url_part),
                make_view(),
                name=make_name()
            ) for url_part in view.get_url_parts()
        ]

    @classmethod
    def get_url_patterns(cls):
        """Get list of URL patterns for all views"""
        urlpatterns = []
        for view in cls.get_views():
            for pattern in cls.get_url_patterns_by_view(view):
                urlpatterns.append(pattern)
        return urlpatterns
