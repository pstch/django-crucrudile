from django.test import TestCase

from .models import ModelInfoMixinTestModel


class AutoPatternsMixinTestCase(TestCase):
    model_class = ModelInfoMixinTestModel

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

