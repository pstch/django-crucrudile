from django.test import TestCase

from .models import TestModel

class TestModelTestCase(TestCase):
    url_func_name = 'get_test_action_url'
    def setUp(self):
        self.model_class = TestModel

    def test_has_url_func(self):
        self.assertTrue(
            hasattr(
                self.model_class,
                self.url_func_name
            )
        )
    def test_url_func_callable(self):
        self.assertTrue(
            callable(
                getattr(
                    self.model_class,
                    self.url_func_name,
                    None
                )
            )
        )
    def test_url_func(self):
        url_func = getattr(
            self.model_class,
            self.url_func_name,
            lambda *args, **kwargs: None
        )
        self.assertEqual(
            url_func(),
            '/testmodel/test-action'
        )
