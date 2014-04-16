"""View mixins classes

This module contains a base view mixin to specify an interface, that
will be used by Model Mixin (in models.mixins) to get informations
about the view :

Action name
  Will be used for URLs, URL names and get_*_url functions. when used
  in URLs or get_*_url functions, it will be underscore-separated,
  otherwise dash-separated.

URL parts
  Will be used for URLs. compiles the multiple possible combinations
  of URL arguments to create a list of possible URL specifications for
  this view (which will be joined to the model name by the model
  mixin).

"""
from django_crucrudile.utils import convert_camel_case


class ModelActionMixin(object):
    r"""This Mixin may be used by any view to indicate parameters for
    the URL, such as the action name (ex: 'list', 'filtered-list',
    'detail', 'create', etc...) and URL arguments (ex: '(?P<pk>\d+)'),
    if needed.

    :param action: action name (examples above), should be
                   dash-separated
    :type action: str
    :param url_args: list of arguments (as used in Django's URL
                     regular expressions)
    :type url_args: list

    """
    action = None
    url_args = None

    @classmethod
    def get_fallback_action_name(cls):
        """Guess a fallback action name, based on the view class name,
        stripped of the tailing 'View', and converted from CamelCase
        (capitalized words) to words_separated_by_underscore.

        :return: fallback action name
        :rtype: str
        """
        class_name = cls.__name__
        if class_name.endswith('View'):
            class_name = class_name[:-4]
        return convert_camel_case(class_name, '-')

    @classmethod
    def get_action_name(cls):
        """Return the action name, using the action attribute of the view, or,
        if not specified, get_fallback_action_name().

        Action name will be cached in cls.action (only computed on first call)

        :return: action name
        :rtype: str
        """
        if cls.action is None:
            cls.action = cls.get_fallback_action_name()
        return cls.action

    @classmethod
    def get_underscored_action_name(cls):
        """Return the underscored action name, which is the same as the action
        name except all dashes are replaced by underscores.

        Used in action-specific function names, and in URL paths.

        :return: underscored action name
        :rtype: str
        """
        return cls.get_action_name().replace('-', '_')

    @classmethod
    def get_url_args(cls):
        """Return the list of regex specifications for URL arguments, as in
        urls.py.  Will be joined with a forward slash ('/').  Can be a
        list of lists, in which case multiple URL patterns will be
        defined (with the same name).

        :return: URL argument specification
        :rtype: list

        """
        return cls.url_args or []

    @classmethod
    def get_url_part(cls, args):
        """Return the URL part for given list of arguments

        :return: compiled URL part
        :rtype: str

        """
        url_part = [cls.get_action_name()] + args
        return "/".join(url_part)

    @classmethod
    def get_url_parts(cls):
        r"""Return a list of possible URL specifications

        (example: 'list', 'detail/(?P<pk>\d+)')

        :return: compiled URL parts
        :rtype: list

        """
        url_args = cls.get_url_args()
        if len(url_args) > 0 and \
           all([True if isinstance(x, list) else False for x in url_args]):
            # url_part is a list of lists of URL args
            return [cls.get_url_part(x) for x in url_args]
        else:
            # url_part is a list of args
            return [cls.get_url_part(url_args)]
