"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.models.mixins.list import ListableModelMixin

from django_pstch_helpers.views import ListView

class ListableModelMixinTestCase(TestCase):
    class TestModel(ListableModelMixin, Model):
        @classmethod
        def get_sort_fields(cls):
            return ['test_sort_field',]
        @classmethod
        def get_paginate_by(cls):
            return 42
        @classmethod
        def get_list_select_related_fields(cls):
            return ['test_related_field',]

    def test_get_views(self):
        self.assertEqual(self.TestModel.get_views(),
                         [ListView])

    def test_get_args_by_view(self):
        self.assertEqual(self.TestModel.get_args_by_view(ListView),
                         {'allowed_sort_fields' : ['test_sort_field',],
                          'paginate_by' : 42,
                          'select_related' : ['test_related_field',]})
