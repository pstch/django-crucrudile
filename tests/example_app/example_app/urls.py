from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .routers import base_router

urlpatterns = patterns(
    '',
    url(r'^', include(
        list(base_router.patterns())
    ))
)
