from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern

from django_crucrudile.exceptions import (
    NoRedirectDefinedException
)

from django_crucrudile.routers import Router, Route


class EmptyRouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        self.base_router = Router()

    def test_patterns_empty(self):
        with self.assertRaises(StopIteration):
            next(self.base_router.patterns())

    def test_redirect_url_name(self):
        with self.assertRaises(NoRedirectDefinedException):
            self.base_router.get_redirect_url_name()

    def test_redirect_pattern(self):
        with self.assertRaises(NoRedirectDefinedException):
            self.base_router.get_redirect_pattern()


class RouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        self.base_router = Router()

        self.documents_router = Router(
            namespace="documents", label="documents"
        )

        self.dashboard_route = Route(redirect="test")

        self.documents_router.register(
            self.dashboard_route, index=True
        )
        self.base_router.register(
            self.documents_router, index=True
        )

    def test_stores(self):
        self.assertEqual(
            self.base_router._store,
            [self.documents_router]
        )
        self.assertEqual(
            self.documents_router._store,
            [self.dashboard_route]
        )

    def test_redirect_url_name(self):
        self.assertEqual(
            self.base_router.get_redirect_url_name(),
            'documents:test'
        )

    def test_redirect_pattern(self):
        self.assertTrue(
            isinstance(
                self.base_router.get_redirect_pattern(),
                RegexURLPattern
            )
        )
gg
