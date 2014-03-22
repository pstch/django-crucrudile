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

