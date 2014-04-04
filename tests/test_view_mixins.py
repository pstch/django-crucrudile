from django.test import TestCase

from tests.views import (
    ModelActionMixinTestView
)


class ModelActionMixinTestCase(TestCase):
    view_class = ModelActionMixinTestView

    def test_get_fallback_action_name(self):
        self.assertEqual(
            self.view_class.get_fallback_action_name(),
            'model-action-mixin-test'
        )

    def test_get_action_name(self):
        self.assertEqual(
            self.view_class.get_action_name(),
            'model-action-mixin-test'
        )

    def test_get_action_name_by_arg(self):
        orig_action = self.view_class.action

        self.view_class.action = 'test-action'
        self.assertEqual(
            self.view_class.get_action_name(),
            'test-action'
        )

        self.view_class.action = orig_action

    def test_get_underscored_action_name(self):
        self.assertEqual(
            self.view_class.get_underscored_action_name(),
            'model_action_mixin_test'
        )

    def test_get_url_args(self):
        self.assertEqual(
            self.view_class.get_url_args(),
            []
        )

    def test_get_url_part(self):
        self.assertEqual(
            self.view_class.get_url_part(),
            'model-action-mixin-test'
        )

    def test_get_url_part_with_args(self):
        @classmethod
        def get_url_args(cls):
            return ['arg1', 'arg2']

        orig_url_args_func = self.view_class.get_url_args

        self.view_class.get_url_args = get_url_args
        self.assertEqual(
            self.view_class.get_url_part(),
            'model-action-mixin-test/arg1/arg2'
        )

        self.view_class.get_url_args = orig_url_args_func
