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
p  of URL arguments to create a list of possible URL specifications for
  this view (which will be joined to the model name by the model
  mixin).

----------------

"""
from django_crucrudile.utils import convert_camel_case


class ActionViewMixin(object):
    _action = None
    _url_specs = None

    def __init__(self, *args, **kwargs):
        # evaluate action when initializing the view so
        # that it's already available when used by the
        # Router
        self.action
        self.url_specs

    def get_action(self):
        class_name = cls.__name__
        if class_name.endswith('View'):
            class_name = class_name[:-4]
        return convert_camel_case(class_name, '-')

    @property
    def action(self):
        """Guess an action name if there is none defined, based on the
        view class name, stripped of the tailing ``View``, and
        converted from ``CamelCase`` (capitalized words) to
        ``words_separated_by_underscore``.

        :return: Fallback action name
        :rtype: str
        """
        if self._action is None:
            self._action = self.get_action()

    @property
    def underscored_action(self):
        """Return the underscored action name, which is the same as the action
        name except all dashes are replaced by underscores.

        Used in action-specific function names, and in URL paths.

        :return: Underscored action name
        :rtype: str
        """
        return self.action.replace('-', '_')

    def get_url_args(self):
        """Return the list of regex specifications for URL arguments, as in
        urls.py.  Will be joined with a forward slash ('/').  Can be a
        list of lists, in which case multiple URL patterns will be
        defined (with the same name).

        :return: URL argument specification
        :rtype: list

        """
        return []

    def _get_url_spec(self, args):
        """Return the URL part for the given list of arguments

        :param args: URL argument specification to compile URL part for
        :type args: list

        :return: Compiled URL part
        :rtype: str

        """
        return "/".join(
            [self.action] if not args else [self.action] + args
        )

    def get_url_specs(self):
        r"""List of possible URL specifications

        Examples : ``['search']``, ``['search/<query regex>']``

        :return: Compiled URL parts
        :rtype: list

        """
        return [self._get_url_spec(x) for x in self.get_url_args()]

    @property
    def url_specs(self):
        if self._url_specs = None:
            self._url_specs = self.get_url_specs()
        return self._url_specs

class ModelViewMixin(ActionViewMixin):
    instance_view = False
    model_view_args = []
    default_instance_view_args = [
        ['(?P<pk>\d+)',],
        ['(?P<slug>[\w-]+)',]
    ]

    def get_url_args(self):
        """Return the list of regex specifications for URL arguments, as in
        urls.py.  Will be joined with a forward slash ('/').  Can be a
        list of lists, in which case multiple URL patterns will be
        defined (with the same name).

        :return: URL argument specification
        :rtype: list

        """
        args = super(ModelActionViewMixin).get_url_args()
            return args + self.default_instance_view_args
        else:
            return args + self.default_model_view_args

class ModelInstanceViewMixin(ModelViewMixin):
    instance_view = True
