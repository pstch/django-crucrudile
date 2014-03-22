def setup_view(view, request, *args, **kwargs):
    """Mimic ``as_view()``, but returns view instance.

    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.

    This is an early implementation of
    https://code.djangoproject.com/ticket/20456

    ``view``
        A view instance, such as ``TemplateView(template_name='dummy.html')``.
        Initialization arguments are the same you would pass to ``as_view()``.

    ``request``
        A request object, typically built with
        :class:`~django.test.client.RequestFactory`.

    ``args`` and ``kwargs``
        "URLconf" positional and keyword arguments, the same you would pass to
        :func:`~django.core.urlresolvers.reverse`.

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

