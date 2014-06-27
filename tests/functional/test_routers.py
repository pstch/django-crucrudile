from django.conf.urls import url, include
from django.test import TestCase

from .routers import base_router


class ResolveTestCase(TestCase):
    router = base_router

    def setUp(self):
        self.patterns = list(self.router.patterns())

    def test_resolve(self):
        _url = url(
            '^/',
            include(self.patterns),
        )
        _url.resolve("/entities/testentitymodel/detail")
