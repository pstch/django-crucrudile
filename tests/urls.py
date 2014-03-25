from django.conf.urls import patterns, include, url

from django_pstch_helpers.views import (
    View,
    TemplateView,
    ListView,
    FilteredListView,
    DetailView,
    CreateView,
    SpecificCreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    TestListableModel,
    TestFilteredListableModel,
    TestDetailableModel,
    TestCreatableModel,
    TestUpdatableModel,
    TestDeletableModel
)

test_patterns = patterns(
    '',
    url(r'^$',
        TemplateView.as_view(template_name="test"),
        name='home'),
    url(r'^test/test-list$',
        ListView.as_view(model=TestListableModel),
        name='test-listable-model-list'),
    url(r'^test/test-filtered-list$',
        FilteredListView.as_view(model=TestFilteredListableModel),
        name='test-filtered-listable-model-filtered-list'),
    url(r'^test/test-detail/(?P<pk>\d+)$',
        DetailView.as_view(model=TestDetailableModel),
        name='test-detailable-model-detail'),
    url(r'^test/test-create$',
        CreateView.as_view(model=TestCreatableModel),
        name='test-creatable-model-create'),
    url(r'^test/test-update/(?P<pk>\d+)$',
        UpdateView.as_view(model=TestUpdatableModel),
        name='test-updatable-model-update'),
    url(r'^test/test-delete/(?P<pk>\d+)$',
        DeleteView.as_view(model=TestDeletableModel),
        name='test-deletable-model-delete'),
)

urlpatterns = patterns(
    '',
    url(r'',
        include(include(test_patterns, namespace="tests", app_name="tests")))
)
