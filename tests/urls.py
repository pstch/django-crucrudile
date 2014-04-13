from django.conf.urls import include, url

from django_crucrudile.utils import auto_patterns_for_app

x = lambda x: None

urlpatterns = [
    url(r"", include(auto_patterns_for_app('tests'))),
]

print urlpatterns
