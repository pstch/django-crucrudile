"""
#TODO: Add module docstring
"""
from django.test import TestCase

from django_pstch_helpers.utils import (get_filter_class,
                                        make_url_name,
                                        contribute_viewset_to_views,
                                        mix_intersection,
                                        mix_views,
                                        get_model_view_args)

from django_pstch_helpers.sets.base import ViewSet

from django_pstch_helpers.views.base import View
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

class ViewSetsUtilsTestCase(TestCase):
    """
    #TODO: Add class docstring
    """
    def test_contribute_viewset_to_views(self):
        """
        #TODO: Add method docstring
        """
        views = {}
        viewset = ViewSet()

        viewset.action = 'action'
        viewset.url = 'url'
        viewset.view = View
        first_tuple = viewset.get_tuple()

        contribute_viewset_to_views(views, viewset)
        self.assertEqual(views,
                         { 'action' : first_tuple})

        viewset.url = 'url2'
        second_tuple = viewset.get_tuple()

        contribute_viewset_to_views(views, viewset)
        self.assertEqual(views,
                         { 'action' : [first_tuple,
                                       second_tuple]})

        viewset.url = 'url2'
        third_tuple = viewset.get_tuple()

        contribute_viewset_to_views(views, viewset)
        self.assertEqual(views,
                         { 'action' : [first_tuple,
                                       second_tuple,
                                       third_tuple]})

        viewset.action = 'action2'
        fourth_tuple = viewset.get_tuple()

        contribute_viewset_to_views(views, viewset)
        self.assertEqual(views,
                         { 'action2' : [first_tuple,
                                       second_tuple,
                                       third_tuple]})

