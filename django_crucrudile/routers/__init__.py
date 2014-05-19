class Router(object):
    url_namespaces = None

    def __init__(self, viewset):
        self.viewset = viewset

    def get_model_name(self):
        """Get the model name
        (example for ``FooBarTestModel`` : 'foobartestmodel')

        :return: Model name
        :rtype: str
        """
        return self.__name__.lower()

    def get_url_namespaces(self, no_content_types=False):
        """Returns the list of URL namespaces to use when creating the URLs.

        To disable usage of URL namespaces, set this to return an
        empty list.  You will need to override this if don't want to
        return the application name as a namespace.

        :param no_content_types: Disable usage of content types framework
                                 (fallback to Django internals
                                 (``model._meta``...))
        :type: no_content_types: bool

        :return: URL namespaces
        :rtype: list

        """
        viewset = self.viewset

        if self.url_namespaces is None:
            try:
                if no_content_types is True:
                    # force fallback to _meta.app_label
                    raise ImportError(
                        "django.contrib.contenttypes import "
                        "explicitly disabled"
                    )
                from django.contrib.contenttypes.models import ContentType
            except ImportError:
                self.url_namespaces = [viewset.model._meta.app_label, ]
            else:
                self.url_namespaces = [
                    ContentType.objects.get_for_model(viewset.model).app_label,
                ]

        return self.url_namespaces
