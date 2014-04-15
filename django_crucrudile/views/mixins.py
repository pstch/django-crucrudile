"""View mixins classes

This module contains a base view mixin to specify an interface, that
will be used by Model Mixin (in models.mixins) to get informations
about the view :

-- action name : will be used for URLs, URL names and get_*_url
functions. when used in URLs or get_*_url functions, it will be
underscore-separated, otherwise dash-separated.

-- url parts : will be used for URLs. compiles the multiple possible
combinations of URL arguments to create a list of possible URL
specifications for this view (which will be joined to the model name
by the model mixin)

Classes :
-- ModelActionMixin : base class for views used by model mixins

Tests:
-- ../../tests/test_view_mixins.py
"""
from django_crucrudile.utils import convert_camel_case

class ModelActionMixin(object):
    """
    #TODO: Add class docstring
    """
    action = None
    url_args = []

    @classmethod
    def get_fallback_action_name(cls):
        """
        #TODO: Add method docstring
        """
        class_name = cls.__name__
        if class_name.endswith('View'):
            class_name = class_name[:-4]
        return convert_camel_case(class_name, '-')

    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        if cls.action is None:
            cls.action = cls.get_fallback_action_name()
        return cls.action

    @classmethod
    def get_underscored_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_action_name().replace('-', '_')

    @classmethod
    def get_url_args(cls):
        """Return the list of regex specifications for URL arguments, as in
        urls.py.  Will be joined with a forward slash ('/').  Can be a
        list of lists, in which case multiple URL patterns will be
        defined (with the same name).

        """
        return cls.url_args or []

    @classmethod
    def get_url_part(cls, args):
        """
        #TODO: Add method docstring
        """
        url_part = [cls.get_action_name()] + args
        return "/".join(url_part)

    @classmethod
    def get_url_parts(cls):
        url_args = cls.get_url_args()
        if len(url_args) > 0 and \
           all([True if isinstance(x, list) else False for x in url_args]):
            # url_part is a list of lists of URL args
            return [cls.get_url_part(x) for x in url_args]
        else:
            # url_part is a list of args
            return [cls.get_url_part(url_args)]
