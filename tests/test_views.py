"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.test.client import RequestFactory
from django.http.response import HttpResponseNotAllowed

from django_pstch_helpers.views import View

from .utils import setup_view

#pylint: disable=R0201, R0903, R0904, W0232, C0103

class ViewTestCase(TestCase):
    view_class = View
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.view = setup_view(self.view_class(),
                               self.request)

    def test_simple_dispatch(self):
        self.assertEqual(type(self.view.dispatch(self.request)),
                         HttpResponseNotAllowed)
    def test_extra_context(self):
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

