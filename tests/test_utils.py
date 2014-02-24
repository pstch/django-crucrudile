"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.utils import (get_filter_class,
                                        make_url_name,
                                        contribute_viewset_to_views,
                                        get_model_view_args)

from django_pstch_helpers.sets.base import ViewSet

from django_pstch_helpers.models.mixins.base import AutoPatternsMixin

from django_pstch_helpers.views.base import View

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
        def _make_test_callable_for_model_view_args_lambda(model, action = 'action',
                                                          return_dict = True):
            def _test_callable_for_model_view_args_lambda(_action, _view, _model):
                self.assertEqual(action, _action)
                self.assertEqual(View, _view)
                self.assertEqual(model, _model)
                if return_dict:
                    return { 'callable_key' : 'callable_value' }
                else:
                    return 'callable_value'
            return _test_callable_for_model_view_args_lambda
        class Model1(AutoPatternsMixin, Model):
            @classmethod
            def get_view_args(cls):
                return {'action' : {'keyword' : 'value'}}
        class Model2(AutoPatternsMixin, Model):
            @classmethod
            def get_view_args(cls):
                return {
                    'action' : {
                        'keyword2' : 'value2'
                    },
                    'action2' : {
                        'keyword' : 'value',
                        'keyword2' : \
                        _make_test_callable_for_model_view_args_lambda(cls, return_dict = False,
                                                                      action = 'action2')
                    }
                }
        class Model3(AutoPatternsMixin, Model):
            @classmethod
            def get_view_args(cls):
                return {'action' : _make_test_callable_for_model_view_args_lambda(cls,
                                                                         action = 'action')}

        model = Model1
        self.assertEqual(get_model_view_args('action', View, model),
                         {'keyword' : 'value'})
        models = [Model1, Model2]
        self.assertEqual(get_model_view_args('action', View, models),
                         {'keyword' : 'value',
                          'keyword2' : 'value2'})
        self.assertEqual(get_model_view_args('action2', View, models),
                         {'keyword' : 'value',
                          'keyword2' : 'callable_value'})
        model = Model3
        self.assertEqual(get_model_view_args('action', View, model),
                         {'callable_key' : 'callable_value'})
