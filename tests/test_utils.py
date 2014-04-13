from django.test import TestCase

from django_crucrudile.utils import auto_patterns_for_app


class AutoPatternsForAppTestCase(TestCase):
    def setUp(self):
        self.patterns = auto_patterns_for_app('tests')

    def test_pattern_name(self):
        self.assertEqual(
            self.patterns[0].name,
            'testmodel-test-action'
        )
    def test_pattern_callback_name(self):
        self.assertEqual(
            self.patterns[0].callback.__name__,
            'TestModelTestView'
        )
    def test_pattern_url(self):
        self.assertEqual(
            self.patterns[0].regex.pattern,
            'tests/testmodel/test-action'
        )
