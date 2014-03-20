"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.models.mixins.list import ListableModelMixin
from django_pstch_helpers.models.mixins.list.filtered import FilteredListableModelMixin
from django_pstch_helpers.models.mixins.detail import DetailableModelMixin

from django_pstch_helpers.views import ListView, FilteredListView, DetailView

class ListableModelMixinTestCase(TestCase):
    class TestListableModel(ListableModelMixin, Model):
        @classmethod
        def get_list_sort_fields(cls):
            return ['test_sort_field',]
        @classmethod
        def get_list_paginate_by(cls):
            return 42
        @classmethod
        def get_list_select_related_fields(cls):
            return ['test_related_field',]

    def test_get_views(self):
        self.assertEqual(self.TestListableModel.get_views(),
                         [ListView])

    def test_get_args_by_view(self):
        self.assertEqual(self.TestListableModel.get_args_by_view(ListView),
                         {'allowed_sort_fields' : ['test_sort_field',],
                          'paginate_by' : 42,
                          'select_related' : ['test_related_field',]})

class FilteredListableModelMixinTestCase(TestCase):
    class TestFilteredListableModel(FilteredListableModelMixin, Model):
        @classmethod
        def get_filtered_list_sort_fields(cls):
            return ['test_sort_field',]
        @classmethod
        def get_filtered_list_paginate_by(cls):
            return 42
        @classmethod
        def get_filtered_list_select_related_fields(cls):
            return ['test_related_field',]

    def test_get_views(self):
        self.assertEqual(self.TestFilteredListableModel.get_views(),
                         [FilteredListView])

    def test_get_args_by_view(self):
        self.assertEqual(
            self.TestFilteredListableModel.get_args_by_view(FilteredListView),
            {'allowed_sort_fields' : ['test_sort_field',],
             'paginate_by' : 42,
             'select_related' : ['test_related_field',]}
        )

class DetailableModelMixinTestCase(TestCase):
    class TestDetailableModel(DetailableModelMixin, Model):
        pass

    def test_get_views(self):
        self.assertEqual(self.TestDetailableModel.get_views(),
                         [DetailView])

