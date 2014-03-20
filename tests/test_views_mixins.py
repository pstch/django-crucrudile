"""
#TODO: Add module docstring
"""
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.views.generic import View

from django.contrib.auth.models import User, AnonymousUser

from django_pstch_helpers.views.mixins.auth import AuthMixin

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

#pylint: disable=R0201, R0903, R0904, W0232, C0103

class AuthMixinTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    class AuthView(AuthMixin, View):
        """
        #TODO: Add class docstring
        """
        pass
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'test',
            'test@localhost.localdomain',
            'test'
        )
        self.view = self.AuthView(required_login=True,
                                  login_template="test/login.html",
                                  template_name="test/home.html")

    def test_required_login_with_valid_user(self):
        """
        #TODO: Add test docstring
        """
        request = self.factory.get('/')

        view = setup_view(self.view,
                          request)

        request.user = self.user

        self.assertTemplateUsed(view.dispatch(request),
                                "test/home.html")

    def test_required_login_without_user(self):
        """
        #TODO: Add test docstring
        """
        request = self.factory.get('/')

        view = setup_view(self.view,
                          request)

        request.user = AnonymousUser()

        self.assertTemplateUsed(view.dispatch(request),
                                "test/login.html")

