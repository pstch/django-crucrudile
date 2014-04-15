from django.conf.urls import include, url

from django_crucrudile.urls import auto_patterns_for_app

x = lambda x: None

urlpatterns = [
    url(r"", include(auto_patterns_for_app('tests'), namespace='tests')),
]
