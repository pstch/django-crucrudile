"""
Model mixin function and base class
===================================

This module contains a base model mixin that defines functions related
to URL pattern generation, and URL handling, and a function that can
create real model mixins (based on the aforementionned base model
mixin) for a given view class.

This module is the main part of ``django-crucrudile``.

----------------

"""
# pylint: disable=W0141, W0142
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf.urls import url

from django_crucrudile.utils import call_if, monkeypatch_mixin
from django_crucrudile.views.mixins import ModelActionMixin


def make_viewset_mixin(view_class,
                     extra_args=None,
                     extra_funcs=None,
                     instance_view=False,
                     no_auto_view_mixin=False):
    """Return a generated Viewset mixin for a given view.

    :param view: View to use for this mixin (this view should subclass
                 ``ModelActionMixin``, if not, and if
                 ``no_auto_view_mixin`` is not set to True,
                 ``ModelActionMixin`` will be monkepatched to the
                 view)
    :type view: django.views.generic.View

    :param extra_args: Dictionary of keyword arguments for the view
                       (the dict value is the argument value,
                       and might be a callable, and will be
                       called with the model as argument)
    :type extra_args: dict

    :param instance_view: Does the view return a Model (List, Create)
                          or an instance of this Model (Detail,
                          Update, Delete) ? If instance, set to True.
    :type instance_view: bool

    :param no_auto_view_mixin: Disable autopatching of view with
                               ``ModelActionMixin``. (When ``view_class``
                               is missing a method or attribute
                               from ``ModelActionMixin``, it is
                               automatically added (and bound if
                               needed). Set this to True to disable
                               this behaviour.)
    :type no_auto_view_mixin: bool

    :return: Viewset mixin for ``view_class``
    :rtype: subclass of ``ViewsetMixin``

    """
    if not no_auto_view_mixin:
        # not inhibiting automatic adding of ModelActionMixin
        # functionality
        view_class = monkeypatch_mixin(view_class, ModelActionMixin)

    class Viewset(AutoPatternsMixin):
        """Class mixin created by make_model_mixin, in order to dynamically
        define the needed functions based on the arguments.

        """
        @classmethod
        def get_views(cls):
            views = super(Viewset, cls).get_views()
            views.append(view_class)
            return views

        @classmethod
        def get_args_by_view(cls, view):
            args = super(Viewset, cls).get_args_by_view(view)
            if view is view_class and extra_args is not None:
                args.update({
                    arg_key: call_if(arg_value, cls)
                    for (arg_key, arg_value) in extra_args.items()
                })
            return args

    def _get_url(obj, *args, **kwargs):
        """Private function, patched as ``get_*_url`` to the model mixin.

        """
        if instance_view or view_class.instance_view:
            kwargs['kwargs'] = kwargs.get('kwargs', {})
            kwargs['kwargs']['pk'] = obj.id

        return reverse(
            obj.get_url_name(view_class, prefix=True),
            *args,
            **kwargs
        )

    _get_url.__doc__ = "Get %s URL" % view_class.get_action_name()
    # we make _get_url a class method only at this point to be able
    # to change __doc__
    if not (instance_view or view_class.instance_view):
        _get_url = classmethod(_get_url)

    setattr(Viewset,
            'get_%s_url' % view_class.get_underscored_action_name(),
            _get_url)

    def _get_url_name(cls):
        """Private function, patched as ``get_*_url_name`` to the model mixin.

        These functions only return an URL name, and you don't have to
        pass an instance as argument because the instance is not
        included in the return value

        """
        return cls.get_url_name(view_class, prefix=True)

    _get_url_name.__doc__ = "Get %s URL" % view_class.get_action_name()

    # we make _get_url_name a class method only at this point to be able
    # to change __doc__
    _get_url_name = classmethod(_get_url_name)

    setattr(Viewset,
            'get_%s_url_name' % view_class.get_underscored_action_name(),
            _get_url_name)

    if extra_funcs:
        for func_name, func in extra_funcs.items():
            func_name = call_if(func_name, view_class)
            setattr(Viewset,
                    func_name,
                    func)

    return Viewset


def make_model_mixins(views,
                      no_auto_view_mixin=False):
    """Return a list of model action mixins for
    the given list of views.

    :param views: Views to make mixins for. Should contain tuples
                  (with at least one item and at most three),
                  themselves containing : **view_class**,
                  **extra_args** (*optional*), **extra_func**
                  (*optional*).  For a definition of the above
                  keywords, please see the documentation of
                  ``make_model_mixin``.

    :type views: list
    :param no_auto_view_mixin: Disable autopatching of view with
                               ModelActionMixin (when view_class is
                               missing a method or attribute from
                               ModelActionMixin, it is automatically
                               added (and bound if needed) to
                               view_class. Set this to True to disable
                               this behaviour. See docs fr more
                               information)
    :type no_auto_view_mixin bool:

    :return: Model action mixins for ``views``
    :rtype: list

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
    url_namespaces = None
    """
    :attribute url_namespaces: List of URL namespaces
    :type url_namespaces: list
    """

    @classmethod
    def get_url_namespaces(cls, no_content_types=False):
        """Returns the list of URL namespaces to use when creating the URLs.

        To disable usage of URL namespaces, set this to return an
        empty list.  You will need to override this if don't want the
        application name as a namespace.

        :param no_content_types: Disable usage of content types framework
                                 (fallback to Django internals
                                 (``model._meta``...))
        :type: no_content_types: bool

        :return: URL namespaces
        :rtype: list

        """

    @classmethod
    def get_url_name(cls, view, prefix=False):
        """Return the URL name for a given view

        Compiles the URL name using ``view.get_action_name`` and
        ``cls.get_model_name``.

        ``get_model_name`` can be None, in which case the URL
        name will be compiled using the action

        :param view: View class to get the URL name for
        :type view:  view class

        :param prefix: Add namespaces prefix to URL name (by default, No)
        :type prefix: bool

        :return: URL name
        :rtype: str

        """
        name = '-'.join(filter(
            None,
            [cls.get_model_name(),
             view.get_action_name()]
        ))

        namespaces_list = cls.get_url_namespaces()
        if prefix and namespaces_list:
            return ':'.join(namespaces_list + [name, ])
        return name

    @classmethod
    def get_url_prefix(cls):
        """Return path prefix

        By default, returns an empty string (so that the URL is
        prefixed directly in urls.py), but it's possible to return a
        prefix based on get_url_namespaces() too.

        :return: URL prefix
        :rtype: str
        """
        return None

    @classmethod
    def get_url_patterns_by_view(cls, view):
        """Get list of URL patterns for a given view and its URL parts
(combinations of URL arguments specification)

        :param view: View to get patterns for
        :type view: view class

        :return: URL patterns of this Model for a given view
        :rtype: list

        :raise ImproperlyConfigured: If view not in :func:`get_views()`


        """

        def make_url(url_part):
            """Make URL pattern (join prefix, model name, and view's URL part)

            """
            return '^%s$' % '/'.join(filter(
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

        if view not in cls.get_views():
            raise ImproperlyConfigured(
                "Tried to get the URL patterns for a view (%s)"
                " that is not defined by get_views" % view
            )

        return [
            url(
                make_url(url_part),
                make_view(),
                name=make_name()
            ) for url_part in view.get_url_parts()
        ]

    @classmethod
    def get_url_patterns(cls, views=None):
        """
        Get list of URL patterns for all views

        :param views: Get URL patterns for these views only.  Each
                      view must be present in the list returned by
                      :func:`get_views`
        :type views: list

        :return: All URL patterns of this Model (for all views, or for
                 views in ``views`` argument)
        :rtype: list

        """
        urlpatterns = []
        for view in views or cls.get_views():
            for pattern in cls.get_url_patterns_by_view(view):
                urlpatterns.append(pattern)
        return urlpatterns
