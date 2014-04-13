from django.test import TestCase

from .models import TestModel

class TestModelTestCase(TestCase):
    def setUp(self):
        self.model_class = TestModel

    def test_has_url_func(self):
        self.assertTrue(
            hasattr(
                self.model_class,
                'get_test_action_url'
            )
        )
