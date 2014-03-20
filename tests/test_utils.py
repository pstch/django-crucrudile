"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.utils import (get_filter_class,
                                        make_url_name)


class FilterUtilsTestCase(TestCase):
    def test_get_filter_class(self):
        class TestModel(Model):
            pass
        class BaseFilterClass(object):
            class Meta:
                pass
        filterset = get_filter_class(TestModel,
                                     BaseFilterClass)
        self.assertEqual(filterset.Meta.model, TestModel)

class URLUtilsTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    def test_make_url_name(self):
        """
        #TODO: Add method docstring
        """
        namespaces = ['namespace1',
                      'namespace2']
        object_url_name = 'objecturlname'
        action = 'action'
        self.assertEqual(make_url_name(namespaces, object_url_name, action),
                         'namespace1:namespace2:objecturlname-action')

        object_url_name = None

        self.assertEqual(make_url_name(namespaces, object_url_name, action),
                         'namespace1:namespace2:action')

        namespaces = None

        self.assertEqual(make_url_name(namespaces, object_url_name, action),
                         'action')
