"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import View as DjangoView

from django.contrib.auth.models import User, AnonymousUser

from django_pstch_helpers.views.mixins.auth import AuthMixin

from .utils import setup_view

#pylint: disable=R0201, R0903, R0904, W0232, C0103

class AuthMixinTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    view_class = DjangoView # Django view because we only test AuthMixin here
    mixin_class = AuthMixin
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'test',
            'test@localhost.localdomain',
            'test'
        )

        class AuthView(self.mixin_class, self.view_class): # pylint: disable=C0111
            pass
        self.view = AuthView(required_login=True,
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

