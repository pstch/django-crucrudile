"""
#TODO: Add module docstring
"""
from django.test import TestCase

from django_pstch_helpers.utils import (get_filter_class,
                                        make_url_name,
                                        contribute_viewset_to_views,
                                        get_model_view_args)

from django_pstch_helpers.sets.base import ViewSet

from django_pstch_helpers.views.mixins.base import AutoPatternsMixin

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

        viewset.url = 'url3'
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
                         { 'action' : [first_tuple,
                                       second_tuple,
                                       third_tuple],
                           'action2' : fourth_tuple})

class ModelAndViewUtilsTestCase(TestCase):
    def test_get_model_view_args(self):
        action = 'action'
        def make_test_callable_for_model_view_args_lambda(model):
            def test_callable_for_model_view_args_lambda(_action, _view, _model):
                self.assertEqual(action, _action)
                self.assertEqual(View, _view)
                self.assertEqual(model, _model)
                return 'callable_value'
            return test_model_view_args_lambda
        class Model1(AutoPatternsMixin):
            def get_view_args(self):
                return {'action' : {'keyword' : 'value'}}
        class Model2(AutoPatternsMixin):
            def get_view_args(self):
                return {
                    'action' : {
                        'keyword2' : 'value2'
                    },
                    'action2' : {
                        'keyword' : 'value',
                        'keyword' : \
                        make_test_callable_for_model_view_args_lambda(self)
                    }
                }
        class Model3(AutoPatternsMixin):
            def get_view_args(self):
                return {'action' : make_test_for_model_view_args_lambda(self)}

        model = Model1
        self.assertEqual(get_model_view_args('action', View, model),
                         {'keyword' : value})
        models = [Model2, Model2]

