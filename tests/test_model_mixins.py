"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model

from django_pstch_helpers.models.mixins.list import ListableModelMixin
from django_pstch_helpers.models.mixins.list.filtered import FilteredListableModelMixin
from django_pstch_helpers.models.mixins.detail import DetailableModelMixin
from django_pstch_helpers.models.mixins.delete import DeletableModelMixin
from django_pstch_helpers.models.mixins.edit import (
    CreatableModelMixin,
    SpecificCreatableModelMixin,
    UpdatableModelMixin
)

from django_pstch_helpers.views import (
    ListView,
    FilteredListView,
    DetailView,
    CreateView,
    SpecificCreateView,
    UpdateView,
    DeleteView
)

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

    def setUp(self):
        self.model = self.TestListableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [ListView])
    def test_get_args_by_view(self):
        self.assertEqual(self.model.get_args_by_view(ListView),
                         {'allowed_sort_fields' : ['test_sort_field',],
                          'paginate_by' : 42,
                          'select_related' : ['test_related_field',]})

class FilteredListableModelMixinTestCase(TestCase):
    class TestFilteredListableModel(FilteredListableModelMixin, Model):
        @classmethod
        def get_filtered_list_sort_fields(cls):
            return ['filtered_test_sort_field',]
        @classmethod
        def get_filtered_list_paginate_by(cls):
            return 24
        @classmethod
        def get_filtered_list_select_related_fields(cls):
            return ['filtered_test_related_field',]

    def setUp(self):
        self.model = self.TestFilteredListableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [FilteredListView])
    def test_get_args_by_view(self):
        self.assertEqual(
            self.model.get_args_by_view(FilteredListView),
            {'allowed_sort_fields' : ['filtered_test_sort_field',],
             'paginate_by' : 24,
             'select_related' : ['filtered_test_related_field',]}
        )

class DetailableModelMixinTestCase(TestCase):
    class TestDetailableModel(DetailableModelMixin, Model):
        pass

    def setUp(self):
        self.model = self.TestDetailableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [DetailView])

class CreatableModelMixinTestCase(TestCase):
    class TestCreatableModel(CreatableModelMixin, Model):
        pass

    def setUp(self):
        self.model = self.TestCreatableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [CreateView])

class SpecificCreatableModelMixinTestCase(TestCase):
    class TestSpecificCreatableModel(SpecificCreatableModelMixin, Model):
        @classmethod
        def get_spec_create_init_keys(cls):
            return ['specific_create_key',]

    def setUp(self):
        self.model = self.TestSpecificCreatableModel

    def test_get_views(self):
        self.assertEqual(
            self.model.get_views(),
            [SpecificCreateView]
        )
    def test_args_by_view(self):
        self.assertEqual(
            self.model.get_args_by_view(SpecificCreateView),
            {'initial_keys' : ['specific_create_key',]}
        )

class UpdatableModelMixinTestCase(TestCase):
    class TestUpdatableModel(UpdatableModelMixin, Model):
        pass

    def setUp(self):
        self.model = self.TestUpdatableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [UpdateView])

class DeletableModelMixinTestCase(TestCase):
    class TestDeletableModel(DeletableModelMixin, Model):
        pass

    def setUp(self):
        self.model = self.TestDeletableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [DeleteView])

class ModelMixinsTestCase(TestCase):
    class TestModel(ListableModelMixin,
                    FilteredListableModelMixin,
                    DetailableModelMixin,
                    CreatableModelMixin,
                    SpecificCreatableModelMixin,
                    UpdatableModelMixin,
                    DeletableModelMixin,
                    Model):
        @classmethod
        def get_list_sort_fields(cls):
            return ['test_sort_field',]
        @classmethod
        def get_list_paginate_by(cls):
            return 42
        @classmethod
        def get_list_select_related_fields(cls):
            return ['test_related_field',]
        @classmethod
        def get_filtered_list_sort_fields(cls):
            return ['filtered_test_sort_field',]
        @classmethod
        def get_filtered_list_paginate_by(cls):
            return 24
        @classmethod
        def get_filtered_list_select_related_fields(cls):
            return ['filtered_test_related_field',]
        @classmethod
        def get_spec_create_init_keys(cls):
            return ['specific_create_key',]

    def setUp(self):
        self.model = self.TestModel

    def test_get_views(self):
        self.assertEqual(
            set(self.model.get_views()),
            set([ListView,
                 FilteredListView,
                 DetailView,
                 CreateView,
                 SpecificCreateView,
                 UpdateView,
                 DeleteView])
        )
    def test_get_args_by_view(self):
        args = {
            ListView : {
                'allowed_sort_fields' : ['test_sort_field',],
                'paginate_by' : 42,
                'select_related' : ['test_related_field',]
            },
            FilteredListView : {
                'allowed_sort_fields' : ['filtered_test_sort_field',],
                'paginate_by' : 24,
                'select_related' : ['filtered_test_related_field',]
            },
            SpecificCreateView : {
                'initial_keys' : ['specific_create_key',]
            }
        }

        for view in args:
            self.assertEqual(
                self.model.get_args_by_view(view),
                args[view]
            )
