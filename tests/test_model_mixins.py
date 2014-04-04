from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.db import models

from django_crucrudile.models.mixins import (
    AutoPatternsMixin,
    make_model_mixin
)

from tests.views import (
    AutoPatternsMixinTestView,
    MakeModelMixinTestView
)

class AutoPatternsMixinTestCase(TestCase):
    class AutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
        @classmethod
        def get_views(cls):
            views = super(
                AutoPatternsMixinTestCase.AutoPatternsMixinTestModel,
                cls
            ).get_views()
            views.append(AutoPatternsMixinTestView)
            return views
    class NoViewsAutoPatternsMixinTestModel(AutoPatternsMixin, models.Model):
        pass

    model_class = AutoPatternsMixinTestModel
    no_views_model_class = NoViewsAutoPatternsMixinTestModel

    def test_get_model_name(self):
        self.assertEqual(
            self.model_class.get_model_name(),
            "autopatternsmixintestmodel"
        )

    def test_get_url_namespaces(self):
        # default namespaces is application name (here, 'tests')
        self.assertEqual(
            self.model_class.get_url_namespaces(),
            ['tests',]
        )

    def test_get_url_name(self):
        # we use the same fake view as ModelActionMixinTestCase
        self.assertEqual(
            self.model_class.get_url_name(AutoPatternsMixinTestView),
            "tests:autopatternsmixintestmodel-auto-patterns-mixin-test"
        )

    def test_get_views(self):
        # by default get_views returns an empty list
        self.assertEqual(
            self.model_class.get_views(),
            [AutoPatternsMixinTestView, ]
        )
        self.assertEqual(
            self.no_views_model_class.get_views(),
            []
        )

    def test_get_args_by_view(self):
        # by defaults args are an empty directory, and when view is
        # not in get_views(), ImproperlyConfigured shall be raised
        try:
            self.no_views_model_class.get_args_by_view(AutoPatternsMixinTestView)
        except ImproperlyConfigured:
            raised = True
        else:
            raised = False
        finally:
            self.assertTrue(raised)

        self.assertEqual(
            self.model_class.get_args_by_view(
                AutoPatternsMixinTestView
            ),
            {}
        )

class MakeModelMixinTestCase(TestCase):
    # data to test basic make_model_mixin with
    model_mixin = make_model_mixin(MakeModelMixinTestView)
    class MakeModelMixinTestModel(
            model_mixin,
            models.Model): pass
    model_class = MakeModelMixinTestModel

    # data to test make_model_mixin (with extra_args argument) with
    extra_args = {'test_key' : 'test_value',
                  'test_callable_key' : lambda model: model.test_callable_value}
    extra_args_called = {'test_key' : 'test_value',
                         'test_callable_key' : 'test_callable_value'}
    extra_args_model_mixin = make_model_mixin(
        MakeModelMixinTestView,
        extra_args=extra_args
    )
    class ExtraArgsMakeModelMixinTestModel(
            extra_args_model_mixin,
            models.Model):
        test_callable_value = 'test_callable_value'
    extra_args_model_class = ExtraArgsMakeModelMixinTestModel

    # data to test make_model_mixin (with extra_funcs argument) with
    @classmethod
    def extra_func(cls):
        return 'extra_func_return'
    # we set up a custom view so that we can be sure that the callable
    # receives the view as argument
    class ExtraFuncMakeModelMixinTestView(MakeModelMixinTestView):
        test_callable_key = 'test_callable_key'
    extra_funcs = {'test_key' : extra_func,
                   lambda view: view.test_callable_key : extra_func}
    extra_funcs_called = {'test_key' : extra_func,
                          'test_callable_key' : extra_func}
    extra_funcs_model_mixin = make_model_mixin(
        ExtraFuncMakeModelMixinTestView,
        extra_funcs=extra_funcs
    )
    class ExtraFuncsMakeModelMixinTestModel(
            extra_funcs_model_mixin,
            models.Model): pass
    extra_funcs_model_class = ExtraFuncsMakeModelMixinTestModel

    def test_make_model_mixin(self):
        self.assertEqual(
            self.model_class.get_views(),
            [MakeModelMixinTestView, ]
        )
        self.assertEqual(
            self.model_class.get_args_by_view(
                MakeModelMixinTestView
            ),
            {}
        )
        self.assertTrue(
            hasattr(self.model_class,
                    'get_make_model_mixin_test_url')
        )
        self.assertEqual(
            getattr(self.model_class,
                    'get_make_model_mixin_test_url',
                    lambda: None)(),
            'tests:makemodelmixintestmodel-make-model-mixin-test'
        )
    def test_make_model_mixin_extra_args(self):
        self.assertEqual(
            self.extra_args_model_class.get_args_by_view(
                MakeModelMixinTestView
            ),
            self.extra_args_called
        )
    def test_make_model_mixin_extra_funcs(self):
        for func in self.extra_funcs_called:
            self.assertTrue(hasattr(self.extra_funcs_model_class, func))
            self.assertEqual(getattr(self.extra_funcs_model_class,
                                     func,
                                     lambda cls: None)(),
                             'extra_func_return')
