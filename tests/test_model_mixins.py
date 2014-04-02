from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from .models import (
    AutoPatternsMixinTestModel,
    AuxAutoPatternsMixinTestModel
)
from .views import (

    AutoPatternsMixinTestView,
    AuxAutoPatternsMixinTestView
)

class AutoPatternsMixinTestCase(TestCase):
    model_class = AutoPatternsMixinTestModel

    def setUp(self):
        self.model = self.model_class()

    def test_get_model_name(self):
        self.assertEqual(
            self.model.get_model_name(),
            "autopatternsmixintestmodel"
        )

    def test_get_url_namespaces(self):
        # default namespaces is application name (here, 'tests')
        self.assertEqual(
            self.model.get_url_namespaces(),
            ['tests',]
        )

    def test_get_url_name(self):
        # we use the same fake view as ModelActionMixinTestCase
        self.assertEqual(
            self.model.get_url_name(AutoPatternsMixinTestView),
            "tests:autopatternsmixintestmodel-auto-patterns-mixin-test"
        )

    def test_get_views(self):
        # by default get_views returns an empty list
        self.assertEqual(
            self.model.get_views(),
            []
        )

    def test_get_args_by_view(self):
        # by defaults args are an empty directory, and when view is
        # not in get_views(), ImproperlyConfigured shall be raised
        try:
            self.model.get_args_by_view(AutoPatternsMixinTestView)
        except ImproperlyConfigured:
            raised = True
        else:
            raised = False

        self.assertTrue(raised)
        self.assertEqual(
            AuxAutoPatternsMixinTestModel.get_args_by_view(AuxAutoPatternsMixinTestView),
            {}
        )

