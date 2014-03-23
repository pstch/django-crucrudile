from django.conf.urls import patterns, include, url

from django_pstch_helpers.views import TemplateView

test_patterns = patterns(
    '',
    url(r'^$',
        TemplateView.as_view(template_name="test"),
        name='home'),
)

urlpatterns = patterns(
    '',
    url(r'^$',
        include((test_patterns, "test", "test")))
)
