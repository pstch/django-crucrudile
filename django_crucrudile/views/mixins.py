"""
View mixin
==========

This module contains a base view mixin to specify an interface, that
will be used by model mixins (in ``models.mixins``) to get metadata
about the view :

**Action name** from :func:`ModelActionMixin.get_action_name`
  Will be used for URLs, URL names and ``get_*_url functions``. when used
  in URLs or ``get_*_url`` functions, it will be underscore-separated,
  otherwise dash-separated.

**URL parts** from :func:`ModelActionMixin.get_url_parts`
  Will be used for URLs. compiles the multiple possible combinations
  of URL arguments to create a list of possible URL specifications for
  this view (which will be joined to the model name by the model
  mixin).

----------------

"""
from django_crucrudile.utils import convert_camel_case


class ModelActionMixin(object):
    r"""This Mixin may be used by any view to set parameters used by
    model mixins for the URL computation, such as the action name
    (e.g., ``list``, ``filtered-list``, ``detail``, ``create``,
    etc...) and URL arguments (ex: ``(?P<pk>\d+)``), if needed.

    """
    action = None
    """
    :attribute action: Action name, should be dash-separated.  (See examples
                 in class documentation)
    :type action: str
    """
    url_args = None
    """
    :attribute url_args: List of arguments (capturing groups, as used in
                   Django's URL regular expressions). (See examples in
                   class documentation)
    :type url_args: list
    """
    instance_view = False
    """
    :attribute url_args: Set to true if the view show an instance
                         (detail, update, delete) rather than a model
                         (list, create)
    :type url_args: bool
    """

    @classmethod
    def get_fallback_action_name(cls):
        """Guess a fallback action name, based on the view class name,
        stripped of the tailing ``View``, and converted from ``CamelCase``
        (capitalized words) to ``words_separated_by_underscore``.

        :return: Fallback action name
        :rtype: str
        """
        class_name = cls.__name__
        if class_name.endswith('View'):
            class_name = class_name[:-4]
        return convert_camel_case(class_name, '-')

    @classmethod
    def get_action_name(cls):
        """Return the action name, using the action attribute of the view, or,
        if not specified, ``get_fallback_action_name()``.

        Action name will be cached in ``cls.action`` (only computed on
        first call)

        :return: Action name
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

        :return: Underscored action name
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

        :param args: URL argument specification to compile URL part for
        :type args: list

        :return: Compiled URL part
        :rtype: str

        """
        url_part = [cls.get_action_name()] + args
        return "/".join(url_part)

    @classmethod
    def get_url_parts(cls):
        r"""Return a list of possible URL specifications

        Examples : ``list``, ``detail/(?P<pk>\d+)``

        :return: Compiled URL parts
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
