from django.conf.urls import patterns, include, url

from django_pstch_helpers.views import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$',
        TemplateView(template_name="test"),
        name='home'),
)
