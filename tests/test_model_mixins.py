"""
#TODO: Add module docstring
"""
from django.core.urlresolvers import Resolver404, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
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
    View,
    ListView,
    FilteredListView,
    DetailView,
    CreateView,
    SpecificCreateView,
    UpdateView,
    DeleteView
)

from django_pstch_helpers.views.mixins.action import ActionMixin

from django_pstch_helpers.models.mixins.base import (
    ModelInfoMixin,
    AutoPatternsMixin
)

class TestModel(Model):
    class Meta:
        abstract = True

class ModelInfoMixinTestCase(TestCase):
    class FaultyModelInfoMixin(ModelInfoMixin):
        pass
    class ModelInfoMixinTestModel(ModelInfoMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.ModelInfoMixinTestModel
        self.faulty_model = self.FaultyModelInfoMixin
        self.object_list = []

        for i in range(20): # pylint: disable=W0612
            instance = self.model().save()
            self.object_list.append(instance)

    def test_get_objects(self):
        self.assertEqual(
            type(self.model._get_objects()),
            Manager
        )

    def test_get_objects_faulty(self):
        raised = False
        try:
            self.faulty_model._get_objects()
        except ImproperlyConfigured:
            raised = True
        self.assertEqual(raised, True)

    def test_get_meta_faulty(self):
        raised = False
        try:
            self.faulty_model._get_meta()
        except ImproperlyConfigured:
            raised = True
        self.assertEqual(raised, True)

    def test_get_meta(self):
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
    class AutoPatternsMixinTestModel(AutoPatternsMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.AutoPatternsMixinTestModel
        self.object_list = []

        for i in range(20): # pylint: disable=W0612
            instance = self.model()
            self.object_list.append(instance)

    def test_get_url_namespaces(self):
        self.assertEqual(self.model.get_url_namespaces(),
                         ['tests'],)
    def test_get_url_name(self):
        self.assertEqual(self.model.get_url_name(),
                         'auto-patterns-mixin-test-model')
    def test_make_url_name(self):
        self.assertEqual(self.model._make_url_name('action'),
                         "tests:auto-patterns-mixin-test-model-action")
    def test_get_url_with_string(self):
        raised = False
        try:
            self.model.get_url('test-action')
        except Resolver404:
            raised = True
        except NoReverseMatch:
            raised = True
        self.assertEqual(raised, True)

    def test_get_url_with_view(self):
        class TestView(ActionMixin, View):
            """We need to add ActionMixin ourselves to the view because it is only included in BaseModelActionMixins."""
            @classmethod
            def get_action_name(cls):
                return 'test-action'
        raised = False
        try:
            self.model.get_url(TestView)
        except Resolver404:
            raised = True
        except NoReverseMatch:
            raised = True
        self.assertEqual(raised, True)

    def test_get_url_with_faulty_view(self):
        raised = False
        try:
            self.model.get_url(View)
        except ImproperlyConfigured:
            raised = True
        self.assertEqual(raised, True)

    def test_get_url_with_faulty_type(self):
        raised = False
        try:
            self.model.get_url(0)
        except TypeError:
            raised = True
        self.assertEqual(raised, True)

    def test_get_views(self):
        self.assertEqual(self.model.get_views(), [])
    def test_get_args_by_view(self):
        self.assertEqual(self.model.get_args_by_view(None), {})

class ListableModelMixinTestCase(TestCase):
    class TestListableModel(ListableModelMixin, TestModel):
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

    def test_get_list_url(self):
        self.assertEqual(self.model.get_list_url(),'/test/test-list')

class FilteredListableModelMixinTestCase(TestCase):
    class TestFilteredListableModel(FilteredListableModelMixin, TestModel):
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
    def test_get_filtered_list_url(self):
        self.assertEqual(self.model.get_filtered_list_url(), '/test/test-filtered-list')


class DetailableModelMixinTestCase(TestCase):
    class TestDetailableModel(DetailableModelMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.TestDetailableModel

        self.instance = self.TestDetailableModel(id=1)
        self.instance.save()

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [DetailView])

    def test_get_detail_url(self):
        self.assertEqual(self.instance.get_detail_url(),'/test/test-detail/1')

    def tearDown(self):
        self.instance.delete()

class CreatableModelMixinTestCase(TestCase):
    class TestCreatableModel(CreatableModelMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.TestCreatableModel

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [CreateView])

    def test_get_create_url(self):
        self.assertEqual(self.model.get_create_url(),'/test/test-create')

class SpecificCreatableModelMixinTestCase(TestCase):
    class SpecificTargetModel(Model):
        pass
    class TestSpecificCreatableModel(SpecificCreatableModelMixin, TestModel):
        @classmethod
        def get_spec_create_init_keys(cls):
            return ['specific_create_key',]

    def setUp(self):
        self.model = self.TestSpecificCreatableModel
        self.target = self.SpecificTargetModel
        self.target_instance = self.target(id=1)
        self.target_instance.save()

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
    def test_get_specific_create_url(self):
        self.assertEqual(
            self.model.get_specific_create_url(self.target_instance),
            '/test/test-specific-create/of-specifictargetmodel/1'
        )

class UpdatableModelMixinTestCase(TestCase):
    class TestUpdatableModel(UpdatableModelMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.TestUpdatableModel

        self.instance = self.TestUpdatableModel(id=1)
        self.instance.save()


    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [UpdateView])

    def test_get_update_url(self):
        self.assertEqual(self.instance.get_update_url(), '/test/test-update/1')

    def test_get_edit_url(self):
        self.assertEqual(self.instance.get_edit_url(), '/test/test-update/1')

    def tearDown(self):
        self.instance.delete()

class DeletableModelMixinTestCase(TestCase):
    class TestDeletableModel(DeletableModelMixin, TestModel):
        pass

    def setUp(self):
        self.model = self.TestDeletableModel

        self.instance = self.TestDeletableModel(id=1)
        self.instance.save()

    def test_get_views(self):
        self.assertEqual(self.model.get_views(),
                         [DeleteView])

    def test_get_delete_url(self):
        self.assertEqual(self.instance.get_delete_url(),'/test/test-delete/1')

    def tearDown(self):
        self.instance.delete()

class TestModelMixinsTestCase(TestCase):
    class AllModelMixinsTestModel(ListableModelMixin,
                    FilteredListableModelMixin,
                    DetailableModelMixin,
                    CreatableModelMixin,
                    SpecificCreatableModelMixin,
                    UpdatableModelMixin,
                    DeletableModelMixin,
                    TestModel):
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
        self.model = self.AllModelMixinsTestModel

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
