class Router(object):
    def __init__(self, views):
        self.views = views

class ModelRouter(object):
    url_namespaces = None

    def __init__(self, views, model):
        self.views = views
        self.model = model

    @property
    def model_name(self):
        """Model name
        (example for ``FooBarTestModel`` : 'foobartestmodel')

        :return: Model name
        :rtype: str
        """
        model = self.model
        return model.__name__.lower()

    @property
    def url_namespaces(self):
        """List of URL namespaces to use when creating the URLs.

        To disable usage of URL namespaces, set this to return an
        empty list.  You will need to override this if you don't want to
        return the application name as a namespace.

        :return: URL namespaces
        :rtype: list

        """
        return [self.model._meta.app_label, ]

    def get_url_name(self, view, prefix=False):
        """Return the URL name for a given view

        Compiles the URL name using ``view.get_action_name`` and
        ``get_model_name``.

        ``get_model_name`` can return None, in which case the URL
        name will be compiled using the action only

        :param view: View class to get the URL name for
        :type view:  view class

        :param prefix: Add namespaces prefix to URL name (by default, No)
        :type prefix: bool

        :return: URL name
        :rtype: str

        """
        name = '-'.join(filter(
            None,
            [self.model_name,
             view.get_action_name()]
        ))

        if prefix and self.url_namespaces:
            return ':'.join(self.url_namespaces + [name, ])
        return name
