"""
#TODO: Add module docstring
"""
from django.test import TestCase
from django.db.models import Model, Manager
from django.db.models.options import Options

from django_pstch_helpers.models.mixins.list import ListableModelMixin
from django_pstch_helpers.models.mixins.list.filtered import FilteredListableModelMixin
from django_pstch_helpers.models.mixins.detail import DetailableModelMixin

from django_pstch_helpers.models.mixins.edit import (
    CreatableModelMixin,
    SpecificCreatableModelMixin,
    UpdatableModelMixin,
    DeletableModelMixin
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

from django_pstch_helpers.models.mixins.base import (
    ModelInfoMixin,
    AutoPatternsMixin
)

class ModelInfoMixinTestCase(TestCase):
    class ModelInfoMixinTestModel(ModelInfoMixin, Model):
        pass

    def setUp(self):
        self.model = self.ModelInfoMixinTestModel
        self.object_list = []

        for i in range(20): # pylint: disable=W0612
            instance = self.model().save()
            self.object_list.append(instance)

    def test__get_objects(self):
        self.assertEqual(
            type(self.model._get_objects()),
            Manager
        )
    def test__get_meta(self):
        self.assertEqual(
            type(self.model._get_meta()),
            Options
        )
    def test_get_verbose_name(self):
        self.assertEqual(
            self.model.get_verbose_name(),
            'model info mixin test model'
        )
    def test_get_count(self):
        self.assertEqual(
            self.model.get_count(),
            20
        )
    def test_get_model_name(self):
        self.assertEqual(
            self.model.get_model_name(),
            'modelinfomixintestmodel'
        )
    def test_get_dashed_verbose_name(self):
        self.assertEqual(
            self.model.get_dashed_verbose_name(),
            'model-info-mixin-test-model'
        )

class AutoPatternsMixinTestCase(TestCase):
    class AutoPatternsMixinTestModel(AutoPatternsMixin, Model):
        pass

    def setUp(self):
        self.model = self.AutoPatternsMixinTestModel
        self.object_list = []

        for i in range(20): # pylint: disable=W0612
            instance = self.model()
            self.object_list.append(instance)

    def test_get_url_prefix(self):
        self.assertEqual(self.model.get_url_prefix(), None)
    def test_get_url_namespaces(self):
        self.assertEqual(self.model.get_url_namespaces(),
                         ['tests'],)
    def test_get_url_name(self):
        self.assertEqual(self.model.get_url_name(),
                         'model-info-mixin-test-model')
    def test__make_url_name(self):
        self.assertEqual(self.model._make_url_name('action'),
                         "tests:model-info-mixin-test-model-action")
    def test_get_url(self):
        #TODO: this
        return
    def test_get_views(self):
        self.assertEqual(self.model.get_views(), [])
    def test_get_args_by_view(self):
        self.assertEqual(self.model.get_args_by_view(None), {})

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

        self.assertEqual(self.model.get_views(),
                         [UpdateView])

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
