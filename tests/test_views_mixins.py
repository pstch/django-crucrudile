"""
#TODO: Add module docstring
"""
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.views.generic import View as DjangoView

from django.contrib.auth.models import User, AnonymousUser

from django_pstch_helpers.views.mixins.auth import AuthMixin
from django_pstch_helpers.views.mixins.action import ActionMixin
from django_pstch_helpers.views.mixins.context import ExtraContextMixin
from django_pstch_helpers.views.mixins.template import (
    TemplateResponseMixin,
    SingleObjectTemplateResponseMixin
)


from django_pstch_helpers.views import View

from .utils import setup_view

#pylint: disable=R0201, R0903, R0904, W0232, C0103

class ActionMixinTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    class ActionMixinTestView(ActionMixin, View):
        """
        #TODO: Add class docstring
        """
        pass

    def setUp(self):
        """
        #TODO: Add method docstring
        """
        self.view_class = self.ActionMixinTestView

    def test_get_action_name(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view_class.get_action_name(),
                         'action-mixin-test')

    def test_get_url_args(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view_class.get_url_args(),
                         [])

    def test_get_url_part(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view_class.get_url_part(),
                         'action-mixin-test')

class ActionMixinWithArgsTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    class ActionMixinWithArgsTestView(ActionMixin, View):
        """
        #TODO: Add class docstring
        """
        @classmethod
        def get_url_args(cls):
            return ['<TEST_ARG>',]

    def setUp(self):
        """
        #TODO: Add method docstring
        """
        self.view_class = self.ActionMixinWithArgsTestView


    def test_get_url_args(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view_class.get_url_args(),
                         ['<TEST_ARG>',])

    def test_get_url_part(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view_class.get_url_part(),
                         'action-mixin-with-args-test/<TEST_ARG>')


class AuthMixinTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    view_class = DjangoView # Django view because we only test AuthMixin here
    mixin_class = AuthMixin
    def setUp(self):
        """
        #TODO: Add method docstring
        """
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

class ExtraContextTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    view_class = DjangoView
    mixin_class = ExtraContextMixin
    def setUp(self):
        """
        #TODO: Add method docstring
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        class ExtraContextView(self.mixin_class, self.view_class): # pylint: disable=C0111
            pass

        self.view = setup_view(ExtraContextView(),
                               self.request)

    def test_extra_context(self):
        """
        #TODO: Add method docstring
        """
        # dict extra context
        test_dict = {'test_key' : 'test_value'}
        self.view.extra_context = test_dict
        self.assertEqual(self.view.get_context_data(),
                         test_dict)
        # callable extra context
        test_lambda = lambda v, c: test_dict
        self.view.extra_context = test_lambda
        self.assertEqual(self.view.get_context_data(),
                         test_dict)
        # dict (with callable values)
        test_dict_callable_values = {'test_key' : lambda v, c: 'test_value'}
        self.view.extra_context = test_dict_callable_values
        self.assertEqual(self.view.get_context_data(),
                         test_dict)
        # callable (which retruns a dict with callable values)
        test_lambda_callable_values = lambda v, c: test_dict_callable_values
        self.view.extra_context = test_lambda_callable_values
        self.assertEqual(self.view.get_context_data(),
                         test_dict)

class TemplateResponseTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    view_class = DjangoView
    mixin_class = TemplateResponseMixin

    def setUp(self):
        """
        #TODO: Add method docstring
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        class TemplateResponseView(self.mixin_class, self.view_class): # pylint: disable=C0111
            pass

        self.view = setup_view(TemplateResponseView(),
                               self.request)

    def test_get_app_name(self):
        """
        #TODO: Add method docstring
        """
        self.assertEqual(self.view.get_app_name(),
                         'tests')

    def test_get_app_prefix(self):
        self.assertEqual(self.view.get_app_prefix(),
                         'tests')

        self.view.app_prefix = 'test_prefix'
        self.assertEqual(self.view.get_app_prefix(),
                         'test_prefix')
        self.view.app_prefix = None

    def test_get_app_prefix_setting(self):
        setattr(settings,
                'PER_APP_TEMPLATE_PREFIX',
                { 'tests' : 'test_prefix'})
        self.assertEqual(self.view.get_app_prefix(),
                         'test_prefix')

        delattr(settings,
                'PER_APP_TEMPLATE_PREFIX')

    def test_prefix_name_if_needed(self):
        self.assertEqual(self.view.prefix_name_if_needed('test_name'),
                         'test_name')

        self.view.template_add_app_prefix = True
        self.assertEqual(self.view.prefix_name_if_needed('test_name'),
                         'tests/test_name')
        self.view.template_add_app_prefix = False

    def test_get_template_names(self):
        raised = False
        try:
            self.view.get_template_names()
        except ImproperlyConfigured:
            raised = True
        self.assertEqual(raised, True)

        self.view.template_name = 'tests/home.html'
        self.assertEqual(self.view.get_template_names(),
                         ['tests/home.html'])
        self.view.template_name = None

class SingleObjectTemplateResponseTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    view_class = DjangoView
    mixin_class = SingleObjectTemplateResponseMixin

    def setUp(self):
        """
        #TODO: Add method docstring
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        class SingleObjectTemplateResponseView(self.mixin_class, self.view_class): # pylint: disable=C0111
            pass

        self.view = setup_view(SingleObjectTemplateResponseView(),
                               self.request)

    def test_get_template_names(self):
        #TODO
        return
